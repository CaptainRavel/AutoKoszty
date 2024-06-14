import datetime
import pandas as pd
from urllib.parse import quote
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpec, UserCars, UserReports
from .forms import CarSelectionForm, UserCarsForm, UserReportsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def priv_pol(request):
    return render(request, 'privacy_policy.html')

def t_o_u(request):
    return render(request, 'terms_of_use.html')

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
    
@login_required
def reports_list(request):
    reports = UserReports.objects.filter(user=request.user)
    add_report_form = UserReportsForm()
    report_forms = {report.id: UserReportsForm(instance=report) for report in reports}
    
    context = {
        'reports': reports,
        'form': add_report_form,
        'report_forms': report_forms,
    }
    return render(request, 'reports_list.html', context)

@login_required
def add_report(request):
    if request.method == 'POST':
        form = UserReportsForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            return redirect('reports_list')
    return redirect('reports_list')

@login_required
def edit_report(request, report_id):
    report = get_object_or_404(UserReports, id=report_id, user=request.user)
    
    if request.method == 'POST':
        form = UserReportsForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            return redirect('reports_list')
    else:
        form = UserReportsForm(instance=report)

    return render(request, 'reports_list.html', {
        'form': form,
        'report': report,  # Dodaj obiekt samochodu do kontekstu renderowania
    })
    
@login_required
def user_reports(request):
    cars = UserCars.objects.filter(user=request.user)
    add_car_form = UserCarsForm()
    car_forms = {car.id: UserCarsForm(instance=car) for car in cars}
    
    context = {
        'cars': cars,
        'form': add_car_form,
        'car_forms': car_forms,
    }
    return render(request, 'user_reports.html', context)

@login_required
def reports_list(request, car_id):
    car = get_object_or_404(UserCars, id=car_id, user=request.user)
    reports = UserReports.objects.filter(car=car)
    add_report_form = UserReportsForm(initial={'car': car})
    edit_report_form = UserReportsForm()  # Pusty formularz do edycji, zostanie zaktualizowany przez JS
    context = {
        'reports': reports,
        'add_report_form': add_report_form,
        'edit_report_form': edit_report_form,
        'car_id': car_id,
    }
    return render(request, 'reports_list.html', context)

@login_required
def add_report(request, car_id):
    car = get_object_or_404(UserCars, id=car_id, user=request.user)
    if request.method == 'POST':
        form = UserReportsForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.car = car
            report.save()
            return redirect('reports_list', car_id=car_id)
    return redirect('reports_list', car_id=car_id)

@login_required
def edit_report(request, report_id, car_id):
    report = get_object_or_404(UserReports, id=report_id, car__id=car_id, car__user=request.user)
    
    if request.method == 'POST':
        form = UserReportsForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            return redirect('reports_list', car_id=car_id)
    else:
        form = UserReportsForm(instance=report)
    
    return render(request, 'edit_report.html', {'form': form, 'report_id': report_id, 'car_id': car_id})

@login_required
def delete_report(request, report_id, car_id):
    report = get_object_or_404(UserReports, id=report_id, car__id=car_id, car__user=request.user)
    
    if request.method == 'POST':
        report.delete()
        return redirect('reports_list', car_id=car_id)
    
    return redirect('reports_list', car_id=car_id)


def get_report_data(request):
    report_id = request.GET.get('report_id')
    report = get_object_or_404(UserReports, id=report_id)  # Pobierz obiekt raportu na podstawie ID
    
    # Przygotuj dane do zwrócenia jako JSON
    data = {
        'report_name': report.report_name,
        'report_type': report.report_type,
        'report_date': report.report_date.strftime('%Y-%m-%d'),  # Formatowanie daty jako string
        'description': report.description if report.description else '',  # Opis raportu
        'price': str(report.price),  # Cena operacji jako string
        'location': report.location if report.location else '',  # Lokalizacja (opcjonalna)
        'file': report.file.url if report.file else '',  # Ścieżka do załączonego pliku (opcjonalna)
    }
    
    return JsonResponse(data)

def generate_summary_xlsx(request, car_id):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    car = get_object_or_404(UserCars, pk=car_id)
    car_name = car.car_name  
    
    reports = UserReports.objects.filter(car_id=car_id, report_date__range=[start_date, end_date])

    data = []
    for report in reports:
        data.append({
            'Nazwa': report.report_name,
            'Typ': report.get_report_type_display(),
            'Data': report.report_date,
            'Cena': report.price,
            'Lokalizacja': report.location,
            'Opis': report.description,
            'Plik': request.build_absolute_uri(report.file.url) if report.file else 'BRAK PLIKU'
        })

    df = pd.DataFrame(data, columns=['Nazwa', 'Typ', 'Data', 'Cena', 'Lokalizacja', 'Opis', 'Plik'])

    # Use a BytesIO buffer to store the Excel file in memory
    from io import BytesIO
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Podsumowanie')

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    encoded_car_name = quote(car_name.encode('utf-8'))

    response['Content-Disposition'] = f'attachment; filename="podsumowanie_raprtów_{encoded_car_name}_{start_date}_-_{end_date}.xlsx"'

    return response

def generate_summary_csv(request, car_id):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        car = get_object_or_404(UserCars, pk=car_id)
        car_name = car.car_name 
    
        reports = UserReports.objects.filter(car_id=car_id, report_date__range=[start_date, end_date])
        
        data = []
        for report in reports:
            data.append({
                'Nazwa': report.report_name,
                'Typ': report.get_report_type_display(),
                'Data': report.report_date,
                'Cena': report.price,
                'Lokalizacja': report.location,
                'Opis': report.description,
                'Plik': request.build_absolute_uri(report.file.url) if report.file else 'BRAK'
            })
        
        df = pd.DataFrame(data)
        
        # Replace semicolons in data with commas
        df = df.applymap(lambda x: str(x).replace(';', ',') if isinstance(x, str) else x)
        
        response = HttpResponse(content_type='text/csv')
        encoded_car_name = quote(car_name.encode('utf-8'))

        response['Content-Disposition'] = f'attachment; filename="podsumowanie_raprtów_{encoded_car_name}_{start_date}_-_{end_date}.csv"'
        
        df.to_csv(response, index=False, sep=';')
        
        return response
  
@login_required 
def user_account(request):
    user = request.user  # Zakładając, że użytkownik jest zalogowany
    context = {
        'user': user
    }
    return render(request, 'user_account.html', context)

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, 'Twoje konto zostało usunięte.')
        return redirect('home_page')  # Przekierowanie na stronę główną lub inną stronę po usunięciu konta
    
    return render(request, 'user_account.html')