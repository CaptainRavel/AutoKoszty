from django.db import models
from django.contrib.auth.models import User

class CarMake(models.Model):
    name = models.CharField(
        max_length=200, 
        unique=True, 
        blank=False,  # Domyślnie False, ale jawnie podajemy
        null=False    # Domyślnie False, ale jawnie podajemy
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car Make"
        verbose_name_plural = "Car Makes"
        ordering = ['name']
        
class CarModel(models.Model):
    make = models.ForeignKey(
        CarMake, 
        on_delete=models.CASCADE, 
        related_name='models', 
        blank=False,  # Pole nie może być puste w formularzach
        null=False,    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    name = models.CharField(
        max_length=200, 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )

    def __str__(self):
        return f'{self.make.name} {self.name}'

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"
        ordering = ['name']

class CarGeneration(models.Model):
    model = models.ForeignKey(
        CarModel, 
        on_delete=models.CASCADE, 
        related_name='generations', 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    name = models.CharField(
        max_length=200, 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    year_begin = models.CharField(
        max_length=200,
        blank=True,  # Pole nie może być puste w formularzach
        null=True    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    year_end = models.CharField(
        max_length=200,
        blank=True,   # Pole może być puste w formularzach, np. dla obecnie produkowanych generacji
        null=True     # Pole może przechowywać wartość NULL w bazie danych
    )

    def __str__(self):
        return f'{self.model.name} {self.name} ({self.year_begin} - {self.year_end if self.year_end else "-"})'

    class Meta:
        verbose_name = "Car Generation"
        verbose_name_plural = "Car Generations"
        ordering = ['model', 'year_begin']
        
class CarSerie(models.Model):
    model = models.ForeignKey(
        CarModel, 
        on_delete=models.CASCADE, 
        related_name='series', 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    generation = models.ForeignKey(
        CarGeneration, 
        on_delete=models.CASCADE, 
        related_name='series', 
        blank=True,  # Pole nie może być puste w formularzach
        null=True    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    name = models.CharField(
        max_length=200, 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )

    def __str__(self):
        return f'{self.model.make.name} {self.model.name} {self.generation.name} {self.name}'

    class Meta:
        verbose_name = "Car Serie"
        verbose_name_plural = "Car Series"
        ordering = ['model', 'generation', 'name']
        

class CarTrim(models.Model):
    serie = models.ForeignKey(
        CarSerie, 
        on_delete=models.CASCADE, 
        related_name='trims', 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    model = models.ForeignKey(
        CarModel, 
        on_delete=models.CASCADE, 
        related_name='trims', 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    name = models.CharField(
        max_length=200, 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    start_production_year = models.CharField(
        max_length=200,
        blank=True,  # Pole nie może być puste w formularzach
        null=True    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    end_production_year = models.CharField(
        max_length=200,
        blank=True,   # Pole może być puste w formularzach, jeśli nie jest znany
        null=True     # Pole może przechowywać wartość NULL w bazie danych
    )

    def __str__(self):
        return f'{self.model.make.name} {self.model.name} {self.serie.name} {self.name} ({self.start_production_year} - {self.end_production_year if self.end_production_year else "present"})'

    class Meta:
        verbose_name = "Car Trim"
        verbose_name_plural = "Car Trims"
        ordering = ['model', 'serie', 'start_production_year']

class CarSpec(models.Model):
    trim = models.ForeignKey(
        'CarTrim', 
        on_delete=models.CASCADE, 
        related_name='specs', 
        blank=False,  
        null=False    
    )
    value = models.CharField(
        max_length=200, 
        blank=True,  
        null=True    
    )
    unit = models.CharField(
        max_length=200, 
        blank=True,  
        null=True    
    )
    spec_name = models.CharField(
        max_length=200, 
        blank=True,  
        null=True    
    )

    def __str__(self):
        return self.spec_name

    class Meta:
        verbose_name = "Car Spec"
        verbose_name_plural = "Car Specs"
        ordering = ['trim']
         
class UserCars(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=100)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField(blank=True, null=True)
    reg_number = models.CharField(max_length=100, blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    oc_date = models.DateField(blank=True, null=True)
    tech_date = models.DateField(blank=True, null=True)
    car_image = models.ImageField(upload_to='static/usr/', blank=True, null=True)

    def __str__(self):
        return f"{self.car_name} ({self.car_make} {self.car_model})"
    
    from django.db import models

class UserReports(models.Model):
    REPORT_TYPE_CHOICES = [
        ('refuel', 'Tankowanie'),
        ('repair', 'Naprawa'),
    ]

    car = models.ForeignKey(UserCars, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    report_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    report_date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='static/usr/', blank=True, null=True)

    def __str__(self):
        return self.report_name