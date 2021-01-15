
from django import forms
from .models import Eq_type, Manufacturer, Eq_model, Eq_mark

class Choose(forms.Form):

    choices = [(obj.name, obj.name) for obj in Manufacturer.objects.all()]

    manufacturer = forms.ChoiceField(required= True, choices = choices)
    eq_model = forms.ChoiceField(required= False)
    eq_type = forms.ChoiceField(required= False)
    eq_mark = forms.ChoiceField(required= False)
    x_coord = forms.FloatField(required = False)
    y_coord = forms.FloatField(required = False)
    

    def __init__(self, ch_manuf = None, ch_model = None, ch_type = None, ch_mark = None,  point_x = None, point_y = None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if ch_manuf:
            manuf_obj = Manufacturer.objects.get(name = ch_manuf)
            self.fields['eq_model'].choices = [(obj.eq_model, obj.eq_model) for obj in Eq_model.objects.filter(manufacturer=manuf_obj)]
            self.fields['manufacturer'].initial = ch_manuf
            
            if ch_model:
                model_obj = Eq_model.objects.get(eq_model = ch_model)
                self.fields['eq_type'].choices = [(obj.eq_type, obj.eq_type) for obj in Eq_type.objects.filter(eq_model = model_obj, manufacturer=manuf_obj)]
                self.fields['eq_model'].initial = ch_model

                if ch_type:
                    type_obj = Eq_type.objects.get(eq_type = ch_type)
                    self.fields['eq_mark'].choices = [(obj.eq_mark, obj.eq_mark) for obj in Eq_mark.objects.filter(eq_type = type_obj)]
                    self.fields['eq_type'].initial = ch_type

                    if ch_mark:
                        self.fields['eq_mark'].initial = ch_mark
        
        if point_x and point_y:
            self.fields['x_coord'].initial = point_x
            self.fields['y_coord'].initial = point_y

class Work_point(forms.Form):
    x_coord = forms.FloatField(required = False)
    y_coord = forms.FloatField(required = False)