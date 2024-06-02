from django.shortcuts import render
from django.http import JsonResponse
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpecValue
from .forms import CarSelectionForm

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
    specs = CarSpecValue.objects.filter(trim_id=trim_id).all()
    return JsonResponse(list(specs.values('spec__name', 'value', 'unit')), safe=False)