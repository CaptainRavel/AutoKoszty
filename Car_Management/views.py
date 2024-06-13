from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpec, UserCars
from .forms import CarSelectionForm, UserCarsForm
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

@login_required
def cars_list(request):
    cars = UserCars.objects.filter(user=request.user)
    add_car_form = UserCarsForm()
    car_forms = {car.id: UserCarsForm(instance=car) for car in cars}
    
    context = {
        'cars': cars,
        'form': add_car_form,
        'car_forms': car_forms,
    }
    return render(request, 'cars_list.html', context)

@login_required
def add_car(request):
    if request.method == 'POST':
        form = UserCarsForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            return redirect('cars_list')
    return redirect('cars_list')

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(UserCars, id=car_id, user=request.user)
    
    if request.method == 'POST':
        form = UserCarsForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('cars_list')
    else:
        form = UserCarsForm(instance=car)

    return render(request, 'cars_list.html', {
        'form': form,
        'car': car,  # Dodaj obiekt samochodu do kontekstu renderowania
    })

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(UserCars, id=car_id, user=request.user)
    if request.method == 'POST':
        car.delete()
        return redirect('cars_list')
    return redirect('cars_list')

def get_car_data(request):
    car_id = request.GET.get('car_id')
    car = UserCars.objects.get(id=car_id)  # Pobierz obiekt samochodu na podstawie ID
    
    # Przygotuj dane do zwrócenia jako JSON
    data = {
        'car_name': car.car_name,
        'car_make': car.car_make,
        'car_model': car.car_model,
        'car_year': car.car_year,
        'reg_number': car.reg_number,
        'mileage': car.mileage,
        'oc_date': car.oc_date,
        'tech_date': car.tech_date,
    }
    
    return JsonResponse(data)

def get_car_models(request):
    try:
        car_make_id = request.GET.get('car_make_id')
        if car_make_id:
            car_models = CarModel.objects.filter(make_id=car_make_id).values('id', 'name')
            return JsonResponse({'car_models': list(car_models)})
        else:
            return JsonResponse({'error': 'Brak parametru car_make_id'})
    except Exception as e:
        return JsonResponse({'error': str(e)})