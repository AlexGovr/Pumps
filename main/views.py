from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import Choose, Work_point
from .models import Manufacturer, EqType, EqModel, EqMark
from .plots import create_plot_image, get_interp_fun, choose_pumps, Curves, formatted


def select(request):
    return render(request, 'main/select.html')

def pumps(request):
    
    manuf = None
    eqtype = None
    eqmodel = None
    eqmark = None
    _x = None
    _y = None
    work_point = None

    if request.method == 'POST':

        manuf = request.POST.get('manufacturer')
        eqtype = request.POST.get('eqtype')
        eqmodel = request.POST.get('eqmodel')
        eqmark = request.POST.get('eqmark')
        _x = request.POST.get('x_coord')
        _y = request.POST.get('y_coord')

    elif request.method == 'GET':

        manuf = request.GET.get('manufacturer')
        eqtype = request.GET.get('eqtype')
        eqmodel = request.GET.get('eqmodel')
        eqmark = request.GET.get('eqmark')
        _x = request.GET.get('x_coord')
        _y = request.GET.get('y_coord')
    
    work_point = (float(_x), float(_y)) if _x  and _y  else None

    context = {}

    if eqmark:
        eqmark_inst = EqMark.objects.get(eqmark=eqmark)
        curves_data = create_plot_image(eqmark_inst, work_point=work_point)
        context.update(curves_data)

    form = Choose(ch_manuf=manuf, ch_model=eqmodel, ch_type=eqtype, ch_mark=eqmark, point_x=_x, point_y=_y)
    context['form'] = form
    return render(request, 'main/pumps.html', context)


def choice(request):

    # in future this will be a choice-field
    eqtype = '1s'
    eqtype_instance = EqType.objects.get(eqtype=eqtype)
    all_marks = EqMark.objects.filter(eqtype=eqtype_instance)

    _x = request.POST.get('x_coord')
    _y = request.POST.get('y_coord')
    work_point = (float(_x), float(_y)) if _x  and _y  else None

    context = {'form': Work_point()}

    choice_data = []

    if work_point:
        try:
            choosen = choose_pumps(all_marks, work_point)
        except ValueError:
            return render(request, 'main/choice.html', {'no_result': True})

        # create output data
        for mark in choosen:
            curves = Curves(mark)
            curves.compute_work_parameters(work_point)
            # make a link
            eqtype = mark.eqtype
            eqmodel = eqtype.eqmodel
            manuf = eqmodel.manufacturer
            link = f'/main?eqmark={mark.eqmark}&eqtype={eqtype.eqtype}&eqmodel={eqmodel.eqmodel}&manufacturer={manuf.name}&x_coord={_x}&y_coord={_y}'

            # pump's name
            info_name = f'{manuf.name} {eqmodel.eqmodel}{eqtype.eqtype}{mark.eqmark}'
            choice_data.append({
                'name': info_name,
                'q_wp': formatted(curves.q_wp),
                'h_wp': formatted(curves.h_wp),
                'npsh_wp': formatted(curves.npsh_wp),
                'eff_wp': formatted(curves.eff_wp),
                'p2_wp': formatted(curves.p2_wp),
                'link': link
            })

        # sort by efficiency
        choice_data.sort(key=lambda x: x['eff_wp'], reverse=True)
        context['choice_data'] = choice_data

    return render(request, 'main/choice.html', context)
