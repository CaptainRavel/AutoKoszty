from django.contrib import admin
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpec, UserCars, UserReports

# Rejestracja modeli za pomocą pętli
for model in [CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpec]:
    admin.site.register(model)
    
for model in [UserCars, UserReports]:
    admin.site.register(model)