'''
set of functions for faster filling of db
usage:
python manage.py runscript fill_db
'''

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from main.models import Manufacturer, EqMark, EqModel, EqType


class InstanceHandler:

    def __init__(self):
        self.info = {}

    def findcreate(self, model, **kwargs):
        key = model.__name__
        try:
            inst = model.objects.get(**kwargs)
            self.__addinfo__(key, 'update')
        except ObjectDoesNotExist:
            inst = model(**kwargs)
            inst.save()
            self.__addinfo__(key, 'new')
        return inst
    
    def __addinfo__(self, key, action):
        if key not in self.info:
            self.info[key] = {
                'new': 0,
                'update': 0,
            }
        self.info[key][action] += 1


def run():
    handler = InstanceHandler()
    manufacturers = ['grundfos', 'dp-pumps']
    for manuf in manufacturers:
        table = pd.read_excel('data/data.xlsx', sheet_name=manuf)
        fill_from_ws(table, manuf, handler)

    print('Updated succefully!')
    print(*handler.info.items(), sep='\n')


def fill_from_ws(table, manuf, handler):


    manuf_inst = handler.findcreate(Manufacturer, name=manuf)
    rows_total = table.count()[0]

    for row in range(rows_total):
        eqmodel = table['model'][row]
        eqtype = table['type'][row]
        eqmark = table['mark'][row]
        dn = table['dn'][row]
        cost = table['cost'][row]
        speed = table['speed'][row]
        q_points = list_by_prefix('q', table, row)
        p2_points = list_by_prefix('p', table, row)
        npsh_points = list_by_prefix('npsh', table, row)
        efficiency_points = list_by_prefix('eff', table, row)
        h_points = list_by_prefix('h', table, row)
        q_optimal = float(table['q_opt'][row])

        model_inst = handler.findcreate(EqModel, eqmodel=eqmodel, manufacturer=manuf_inst)
        type_inst = handler.findcreate(EqType, eqmodel=model_inst, 
                                        eqtype=eqtype, 
                                        manufacturer=manuf_inst)
        mark_inst = handler.findcreate(EqMark, eqmark=eqmark, 
                                        manufacturer=manuf_inst, 
                                        eqtype=type_inst, 
                                        eqmodel=model_inst)
        # assign if new mark or change if existing one
        mark_inst.h_curve_points = ','.join(h_points)
        mark_inst.q_curve_points = ','.join(q_points)
        mark_inst.p2_curve_points = ','.join(p2_points)
        mark_inst.npsh_curve_points = ','.join(npsh_points)
        mark_inst.efficiency_curve_points = ','.join(efficiency_points)
        mark_inst.q_optimal = q_optimal
        mark_inst.dn=dn
        mark_inst.cost=cost
        mark_inst.speed=speed
        mark_inst.save()

def list_by_prefix(prefix, table, row):
    i = 0
    colname = f'{prefix}{i}'
    ls = []
    while colname in table:
        ls.append(str(table[colname][row]))
        i += 1
        colname = f'{prefix}{i}'
    return ls