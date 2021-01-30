
from django import forms
from .models import EqType, Manufacturer, EqModel, EqMark



class Choose(forms.Form):

    choices = [(obj.name, obj.name) for obj in Manufacturer.objects.all()]

    manufacturer = forms.ChoiceField(required= True, choices=choices)
    eqmodel = forms.ChoiceField(required=False)
    eqtype = forms.ChoiceField(required=False)
    eqmark = forms.ChoiceField(required=False)
    x_coord = forms.FloatField(required=False)
    y_coord = forms.FloatField(required=False)
    

    def __init__(self, ch_manuf=None, ch_model=None, ch_type=None, ch_mark=None,  point_x=None, point_y=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # simple implementation of chained choice
        if ch_manuf:
            manuf_obj = Manufacturer.objects.get(name=ch_manuf)
            self.fields['eqmodel'].choices = [(obj.eqmodel, obj.eqmodel) for obj in EqModel.objects.filter(manufacturer=manuf_obj)]
            self.fields['manufacturer'].initial = ch_manuf
            
            if ch_model:
                model_obj = EqModel.objects.get(eqmodel=ch_model)
                self.fields['eqtype'].choices = [(obj.eqtype, obj.eqtype) for obj in EqType.objects.filter(eqmodel=model_obj, manufacturer=manuf_obj)]
                self.fields['eqmodel'].initial = ch_model

                if ch_type:
                    type_obj = EqType.objects.get(eqtype=ch_type)
                    self.fields['eqmark'].choices = [(obj.eqmark, obj.eqmark) for obj in EqMark.objects.filter(eqtype=type_obj)]
                    self.fields['eqtype'].initial = ch_type

                    if ch_mark:
                        self.fields['eqmark'].initial = ch_mark
        
        if point_x and point_y:
            self.fields['x_coord'].initial = point_x
            self.fields['y_coord'].initial = point_y


class Work_point(forms.Form):
    x_coord = forms.FloatField(required=False)
    y_coord = forms.FloatField(required=False)