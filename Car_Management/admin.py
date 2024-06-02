from django.contrib import admin
from .models import CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpecValue, CarSpec

# Rejestracja modeli za pomocą pętli
for model in [CarMake, CarModel, CarGeneration, CarSerie, CarTrim, CarSpecValue, CarSpec]:
    admin.site.register(model)