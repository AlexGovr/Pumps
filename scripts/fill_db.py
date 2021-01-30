'''
set of functions for faster filling of db
usage:
python manage.py runscript fill_db
'''

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from main.models import Manufacturer, EqMark, EqModel, EqType


def run():

    manufacturer = 'grundfos'
    eqmodel = 'CR'
    eqtype = '1s'
    manuf_inst = Manufacturer.objects.get(name = manufacturer)

    table = pd.read_excel('data/data.xlsx', sheet_name = manufacturer)
    rows_total = table.count()[0]
    points_count = 6

    try:
        model_inst = EqModel.objects.get(manufacturer = manuf_inst, eqmodel = eqmodel)
    except ObjectDoesNotExist:
        model_inst = EqModel(manufacturer = manuf_inst, eqmodel = eqmodel)
        model_inst.save()
    
    try:
        type_inst = EqType.objects.get(eqmodel = model_inst, eqtype = eqtype, manufacturer=manuf_inst)
    except ObjectDoesNotExist:
        type_inst = EqType(eqmodel = model_inst, eqtype = eqtype, manufacturer=manuf_inst)
        type_inst.save()

    for row in range(rows_total):
        eqmark = table['mark'][row]
        q_points = [str(table[f'q{point}'][row]) for point in range(points_count)]
        p2_points = [str(table[f'p{point}'][row]) for point in range(points_count)]
        npsh_points = [str(table[f'npsh{point}'][row]) for point in range(points_count)]
        efficiency_points = [str(table[f'eff{point}'][row]) for point in range(points_count)]
        h_points = [str(table[f'h{point}'][row]) for point in range(points_count)]  

        try:
            mark_inst = EqMark.objects.get(eqmark = eqmark, manufacturer = manuf_inst, eqtype = type_inst)
        except ObjectDoesNotExist:
            mark_inst = EqMark(eqmark = eqmark, manufacturer = manuf_inst, eqtype = type_inst, eqmodel=model_inst)
        
        mark_inst.h_curve_points = ','.join(h_points)
        mark_inst.q_curve_points = ','.join(q_points)
        mark_inst.p2_curve_points = ','.join(p2_points)
        mark_inst.npsh_curve_points = ','.join(npsh_points)
        mark_inst.efficiency_curve_points = ','.join(efficiency_points)
        mark_inst.save()

    print('Updated succefully!')