from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=60, blank=True, default='Unnamed')


class EqModel(models.Model):
    eqmodel = models.CharField(max_length=30, blank=True, default='Unnamed')
    manufacturer = models.ForeignKey(Manufacturer, on_delete= models.CASCADE)


class EqType(models.Model):
    eqtype = models.CharField(max_length=30, blank=True, default='Unnamed')
    eqmodel = models.ForeignKey(EqModel, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)


class EqMark(models.Model):
    eqmark = models.CharField(max_length=60, blank=True, default='Unnamed')
    eqtype = models.ForeignKey(EqType, on_delete=models.CASCADE)
    eqmodel = models.ForeignKey(EqModel, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    dn = models.CharField(max_length=10, default='not_specified')
    cost = models.CharField(max_length=10, default='not_specified')
    speed = models.CharField(max_length=10, default='not_specified')

    # curves fields
    default_curve_string = ','.join(['0.00']*8)
    h_curve_points = models.CharField(max_length=150, blank=True, default=default_curve_string)
    q_curve_points = models.CharField(max_length=150, blank=True, default=default_curve_string)
    p2_curve_points = models.CharField(max_length=150, blank=True, default=default_curve_string)
    npsh_curve_points = models.CharField(max_length=150, blank=True, default=default_curve_string)
    efficiency_curve_points = models.CharField(max_length=150, blank=True, default=default_curve_string)
    q_optimal = models.FloatField(default=0)