import os
import pandas as pd
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .forms import Choose, Work_point
from .models import Manufacturer, Eq_type, Eq_model, Eq_mark
from .plots import create_plot_image, get_interp_fun, choose_pumps, Curves, formatted



def pumps(request):
    
    manuf = None
    eq_type = None
    eq_model = None
    eq_mark = None
    _x = None
    _y = None
    work_point = None

    if request.method == 'POST':

        manuf = request.POST.get('manufacturer')
        eq_type = request.POST.get('eq_type')
        eq_model = request.POST.get('eq_model')
        eq_mark = request.POST.get('eq_mark')
        _x = request.POST.get('x_coord')
        _y = request.POST.get('y_coord')

    elif request.method == 'GET':

        manuf = request.GET.get('manufacturer')
        eq_type = request.GET.get('eq_type')
        eq_model = request.GET.get('eq_model')
        eq_mark = request.GET.get('eq_mark')
        _x = request.GET.get('x_coord')
        _y = request.GET.get('y_coord')
    
    work_point = (float(_x), float(_y)) if _x  and _y  else None

    context = {}

    if eq_mark:
        eq_mark_inst = Eq_mark.objects.get(eq_mark = eq_mark)
        curves_data = create_plot_image(eq_mark_inst, work_point = work_point)
        context.update(curves_data)

    form = Choose(ch_manuf = manuf, ch_model = eq_model, ch_type = eq_type, ch_mark = eq_mark, point_x = _x, point_y = _y)
    context['form'] = form
    return render(request, 'main/pumps.html', context)

def choice(request):

    # this should be a choice-field
    eq_type = '1s'

    eq_type_instance = Eq_type.objects.get(eq_type = eq_type)

    all_marks = Eq_mark.objects.filter(eq_type = eq_type_instance)

    _x = request.POST.get('x_coord')
    _y = request.POST.get('y_coord')
    work_point = (float(_x), float(_y)) if _x  and _y  else None

    context = {}
    context['form'] = Work_point()

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
            eq_type = mark.eq_type

            eq_model = eq_type.eq_model

            manuf = eq_model.manufacturer

            link = f'/main?eq_mark={mark.eq_mark}&eq_type={eq_type.eq_type}&eq_model={eq_model.eq_model}&manufacturer={manuf.name}&x_coord={_x}&y_coord={_y}'

            # pump's name
            info_name = f'{manuf.name} {eq_model.eq_model}{eq_type.eq_type}{mark.eq_mark}'

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
        choice_data.sort(key = lambda x: x['eff_wp'], reverse = True)

        context['choice_data'] = choice_data

    return render(request, 'main/choice.html', context)

def update_data(request):

    manufacturer = 'Grundfos'
    eq_model = 'CR'
    eq_type = '1s'
    manuf_inst = Manufacturer.objects.get(name = manufacturer)

    table = pd.read_excel('Data/data.xlsx', sheet_name = manufacturer)
    rows_total = table.count()[0]
    points_count = 6

    try:
        model_inst = Eq_model.objects.get(manufacturer = manuf_inst, eq_model = eq_model)
    except ObjectDoesNotExist:
        model_inst = Eq_model(manufacturer = manuf_inst, eq_model = eq_model)
        model_inst.save()
    
    try:
        type_inst = Eq_type.objects.get(eq_model = model_inst, eq_type = eq_type)
    except ObjectDoesNotExist:
        type_inst = Eq_type(eq_model = model_inst, eq_type = eq_type)
        type_inst.save()

    for row in range(rows_total):
        eq_mark = table['mark'][row]
        q_points = [str(table[f'q{point}'][row]) for point in range(points_count)]
        p2_points = [str(table[f'p2{point}'][row]) for point in range(points_count)]
        npsh_points = [str(table[f'npsh{point}'][row]) for point in range(points_count)]
        efficiency_points = [str(table[f'eff{point}'][row]) for point in range(points_count)]
        h_points = [str(table[f'h{point}'][row]) for point in range(points_count)]

        try:
            mark_inst = Eq_mark.objects.get(eq_mark = eq_mark, manufacturer = manuf_inst, eq_type = type_inst)
        except ObjectDoesNotExist:
            mark_inst = Eq_mark(eq_mark = eq_mark, manufacturer = manuf_inst, eq_type = type_inst)
        
        mark_inst.h_curve_points = ','.join(h_points)
        mark_inst.q_curve_points = ','.join(q_points)
        mark_inst.p2_curve_points = ','.join(p2_points)
        mark_inst.npsh_curve_points = ','.join(npsh_points)
        mark_inst.efficiency_curve_points = ','.join(efficiency_points)
        mark_inst.save()

    print('Updated succefully!')
    
    return render(request, 'main/pumps.html')