
import numpy as np
from scipy.interpolate import interp1d
from random import choices

# prevent runtime error
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt


class Curves():

    def __init__(self, mark_inst, interplolate_curves=True, interp_points=40):
        self.q_points_coarse = get_list_points(mark_inst.q_curve_points)
        self.q_points = np.linspace(self.q_points_coarse[0], self.q_points_coarse[-1], interp_points, endpoint=True)
        self.q_points = list(self.q_points)

        # interpolate curves
        self.h_fun = get_interp_fun(mark_inst, 'h')
        self.eff_fun = get_interp_fun(mark_inst, 'eff')
        self.npsh_fun = get_interp_fun(mark_inst, 'npsh')
        self.p2_fun = get_interp_fun(mark_inst, 'p2')

        self.h_points = None
        self.eff_points = None
        self.npsh_points = None
        self.p2_points = None
        # compute optimal point
        _q_opt = mark_inst.q_optimal
        _h_opt = self.h_fun(_q_opt)
        self.work_point_opt = (_q_opt, _h_opt)

        if interplolate_curves:
            self.h_points = self.h_fun(self.q_points)
            self.eff_points = self.eff_fun(self.q_points)
            self.npsh_points = self.npsh_fun(self.q_points)
            self.p2_points = self.p2_fun(self.q_points)

        self.work_point = None
        self.h_load_fun = None
        self.h_load_points = None
        self.h_wp = None
        self.q_wp = None
        self.eff_wp = None
        self.npsh_wp = None
        self.p2_wp = None

    def compute_work_parameters(self, work_point=None):
        
        if work_point is None:
            work_point = self.work_point_opt
        self.work_point = work_point
        if not (self.work_point[0] > 0 and self.work_point[1]) > 0:
            raise Exception('Invalid work point!')

        # compute and plot load curve
        koef = self.work_point[1]/self.work_point[0]**2
        self.h_load_points = [koef*q**2 for q in self.q_points]
        self.h_load_fun = get_interp_fun(x_points=self.q_points, y_points=self.h_load_points)
        self.q_wp, self.h_wp = get_intersect_point(self.h_fun, self.h_load_fun, segment=(self.q_points[0], self.q_points[-1]))

        if self.q_wp:
            self.h_wp = float(self.h_wp)
            # compute other curves' values
            self.eff_wp = float(self.eff_fun(self.q_wp))
            self.npsh_wp = float(self.npsh_fun(self.q_wp))
            self.p2_wp = float(self.p2_fun(self.q_wp))


def get_interp_fun(mark_inst=None, which_curve='', interp_kind='quadratic', x_points=None, y_points=None):

    if y_points == None:
        if not which_curve:
            raise Exception('which_curve must be assigned if y_points is None')
        if not mark_inst:
            raise Exception('mark_inst must be assigned if y_points is None')

        if which_curve == 'h':
            y_points = mark_inst.h_curve_points
        elif which_curve == 'eff':
            y_points = mark_inst.efficiency_curve_points
        elif which_curve == 'p2':
            y_points = mark_inst.p2_curve_points
        elif which_curve == 'npsh':
            y_points = mark_inst.npsh_curve_points

        y_points = get_list_points(y_points)

    if x_points == None:
        x_points = get_list_points(mark_inst.q_curve_points)

    return interp1d(x_points, y_points, kind=interp_kind)


def create_plot_image(mark_inst, work_point=None):

    truncate_koef = 1.2
    path1 = '/static/images/pq_and_eff.png'
    path2 = '/static/images/npsh.png'
    path3 = '/static/images/p2.png'
    curves = Curves(mark_inst, interplolate_curves=True)
    
    # clean plots
    plt.clf() 
    # plot H-Q curve
    plt.plot(curves.q_points, curves.h_points)

    # plot workpoint and load H-Q curve
    if work_point:
        curves.compute_work_parameters(work_point)
        # plot work_point
        plt.plot(curves.work_point[0], curves.work_point[1], 'ro')

        if curves.q_wp:
            q_points = curves.q_points
            # compute index to truncate load curve
            i = 0
            while q_points[i] < curves.q_wp:
                i += 1
            i = round(i*truncate_koef)
            # plot curve truncated
            plt.plot(q_points[:i], curves.h_load_points[:i])
            plt.plot(curves.q_wp, curves.h_wp, 'ro')

    # plot eff-Q curve
    ax_eff = plt.twinx()
    ax_eff.plot(curves.q_points, curves.eff_points)
    # get efficiency max value
    eff_max = max(curves.eff_points)
    # set plot y lim(it
    ax_eff.set_ylim((0, eff_max*3))
    plt.savefig('Main/' + path1)
    
    # plot npsh-Q curve
    plt.clf()
    plt.plot(curves.q_points, curves.npsh_points)
    plt.savefig('Main/' + path2)

    # plot p2-Q curve
    plt.clf()
    plt.plot(curves.q_points, curves.p2_points)
    plt.savefig('Main/' + path3)

    curves_data = {
        'img1': path1,
        'img2': path2,
        'img3': path3
    }

    if curves.q_wp != None:
        
        extra = {
            'q_wp': formatted(curves.q_wp),
            'h_wp': formatted(curves.h_wp),
            'eff_wp': formatted(curves.eff_wp),
            'npsh_wp': formatted(curves.npsh_wp),
            'p2_wp': formatted(curves.p2_wp)
        }

        curves_data.update(extra)
    
    return curves_data


def get_list_points(str_curve):
    '''
    converts string of comma-separated floats into a list of floats
    :input: [str]
    :returns: a list of floats
    '''
    return [float(s) for s in str_curve.split(',')]


def get_intersect_point(f1, f2, segment, tol=0.001, max_iters=100):
    max_x = segment[1]
    min_x = segment[0]
    if f1(min_x) < f2(min_x):
        f1, f2 = f2, f1
    x = (max_x - min_x)*0.5
    y1 = f1(x)
    y2 = f2(x)
    diff = y1 - y2

    while (abs(diff) > tol) and max_iters:
        max_iters -= 1
        if diff > 0:
            min_x = x
            x = x + (max_x - x)*0.5
            y1 = f1(x)
            y2 = f2(x)
            diff = y1 - y2
        else:
            max_x = x
            x = x - (x - min_x)*0.5
            y1 = f1(x)
            y2 = f2(x)
            diff = y1 - y2

    if not max_iters and (abs(diff) > tol):
        return None, None

    return x, y1


def choose_pumps(all_marks, work_point):
    '''
    :input: all_marks - list of EqMark objects
    :input: work_point - tuple (wpq, wph)
    :return: list of EqMark objects
    '''
    q, h = work_point
    choosen = []
    additional = {}
    # choose siutable marks
    curves = None
    for mark in all_marks:
        curves = Curves(mark)
        curves.compute_work_parameters(work_point)
        actual_h = curves.h_wp

        if not actual_h:
            continue
        delta = h/actual_h

        if 0.5 < delta < 1.02:
            choosen.append(mark)
            add = {
                'q_wp': curves.q_wp,
                'h_wp': curves.h_wp,
                'q_ratio': curves.q_wp/mark.q_optimal,
                'eff_wp': curves.eff_wp,
                'p2_wp': curves.p2_wp,
                'npsh_wp': curves.npsh_wp,
            }
            # format additional_data
            add = {k:formatted(v) for (k, v) in add.items()}
            additional[mark.id] = add

    q_load = curves.q_points_coarse
    h_load = [curves.h_load_fun(q) for q in q_load]

    return choosen, best_solutions(choosen), additional, q_load, h_load


def best_solutions(choosen):
    result = {
        'energy': max(choosen, key=work_efficiency).id,
        'cost': min(choosen, key=lambda m: m.cost).id,
        'delivery': choosen[0].id,
        'weight': min(choosen, key=lambda m: m.mass).id,
    }
    return result


def work_efficiency(mark):
    curves = Curves(mark)
    curves.compute_work_parameters()
    return curves.eff_wp


def formatted(f):
    return '{:.2f}'.format(f)