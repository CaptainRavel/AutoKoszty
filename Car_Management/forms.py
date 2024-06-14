from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim, UserCars, UserReports

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

class UserCarsForm(forms.ModelForm):
    class Meta:
        model = UserCars
        fields = ['car_name', 'car_make', 'car_model', 'car_year', 'reg_number', 'mileage', 'oc_date', 'tech_date', 'car_image']
        labels = {
            'car_name': 'Nazwa auta',
            'car_make': 'Marka auta',
            'car_model': 'Model auta',
            'car_year': 'Rok produkcji',
            'reg_number': 'Numer rejestracyjny',
            'mileage': 'Przebieg',
            'oc_date': 'Data OC',
            'tech_date': 'Data przeglądu technicznego',
            'car_image': 'Zdjęcie auta'
        }
        widgets = {
            'car_name': forms.TextInput(attrs={'class': 'form-control'}),
            'car_make': forms.TextInput(attrs={'class': 'form-control'}),
            'car_model': forms.TextInput(attrs={'class': 'form-control'}),
            'car_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'reg_number': forms.TextInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'oc_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tech_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'car_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserReportsForm(forms.ModelForm):
    class Meta:
        model = UserReports
        fields = ['report_type', 'report_name', 'description', 'price', 'report_date', 'location', 'file']
        labels = {
            'report_type': 'Typ raportu',
            'report_name': 'Nazwa raportu',
            'description': 'Opis',
            'price': 'Cena',
            'report_date': 'Data',
            'location': 'Miejsce',
            'file': 'Dodaj plik',
        }
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'report_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'report_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }