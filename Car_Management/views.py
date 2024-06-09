from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpec
from .forms import CarSelectionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def home_page(request):
    return render (request, 'home.html')

def cars_base(request):
    return render (request, 'cars_base.html')

def calculators(request):
    return render (request, 'calculators.html')

def car_selection_view(request):
    form = CarSelectionForm()
    return render(request, 'cars_base.html', {'form': form})

def load_models(request):
    make_id = request.GET.get('make')
    models = CarModel.objects.filter(make_id=make_id).all()
    return JsonResponse(list(models.values('id', 'name')), safe=False)

def load_generations(request):
    model_id = request.GET.get('model')
    generations = CarGeneration.objects.filter(model_id=model_id).all()
    return JsonResponse(list(generations.values('id', 'name')), safe=False)

def load_series(request):
    generation_id = request.GET.get('generation')
    series = CarSerie.objects.filter(generation_id=generation_id).all()
    return JsonResponse(list(series.values('id', 'name')), safe=False)

def load_trims(request):
    serie_id = request.GET.get('serie')
    trims = CarTrim.objects.filter(serie_id=serie_id).all()
    return JsonResponse(list(trims.values('id', 'name')), safe=False)

def load_specs(request):
    trim_id = request.GET.get('trim')
    specs = CarSpec.objects.filter(trim_id=trim_id).all()
    return JsonResponse(list(specs.values('spec_name', 'value', 'unit')), safe=False)

def login_view(request):
    invalid = False  # Domyślnie ustawiamy zmienną invalid na False
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_page')  # Przekieruj na stronę po zalogowaniu
        invalid = True  # Jeśli logowanie nie powiodło się, ustaw invalid na True
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'invalid': invalid})  # Przesyłamy invalid do szablonu

def logout_view(request):
    logout(request)
    return redirect('home_page')  # Przekieruj na stronę po wylogowaniu

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})