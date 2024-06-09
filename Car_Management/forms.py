from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim

class CarSelectionForm(forms.Form):
    make = forms.ModelChoiceField(queryset=CarMake.objects.all(), empty_label="----------")
    model = forms.ModelChoiceField(queryset=CarModel.objects.none(), empty_label="----------")
    generation = forms.ModelChoiceField(queryset=CarGeneration.objects.none(), empty_label="----------")
    serie = forms.ModelChoiceField(queryset=CarSerie.objects.none(), empty_label="----------")
    trim = forms.ModelChoiceField(queryset=CarTrim.objects.none(), empty_label="----------")
    
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Adres email", required=True, help_text="Wprowadź ważny adres email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nazwa użytkownika',
            'password1': 'Hasło',
            'password2': 'Potwierdź hasło'
        }
        help_texts = {
            'username': ' ',
        }