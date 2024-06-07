from django import forms
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim

class CarSelectionForm(forms.Form):
    make = forms.ModelChoiceField(queryset=CarMake.objects.all(), empty_label="----------")
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), empty_label="----------")
    generation = forms.ModelChoiceField(queryset=CarGeneration.objects.none(), empty_label="----------")
    serie = forms.ModelChoiceField(queryset=CarSerie.objects.none(), empty_label="----------")
    trim = forms.ModelChoiceField(queryset=CarTrim.objects.none(), empty_label="----------")