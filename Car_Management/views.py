from django.shortcuts import render


# Create your views here.

def home_page(request):
    return render (request, 'home.html')

def cars_base(request):
    return render (request, 'cars_base.html')

def calculators(request):
    return render (request, 'calculators.html')
