from django.db import models

class CarMake(models.Model):
    name = models.CharField(
        max_length=255, 
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
        max_length=255, 
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
        max_length=255, 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    year_begin = models.PositiveIntegerField(
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    year_end = models.PositiveIntegerField(
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
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    name = models.CharField(
        max_length=255, 
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
        max_length=255, 
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    start_production_year = models.PositiveIntegerField(
        blank=False,  # Pole nie może być puste w formularzach
        null=False    # Pole nie może przechowywać wartości NULL w bazie danych
    )
    end_production_year = models.PositiveIntegerField(
        blank=True,   # Pole może być puste w formularzach, jeśli nie jest znany
        null=True     # Pole może przechowywać wartość NULL w bazie danych
    )

    def __str__(self):
        return f'{self.model.make.name} {self.model.name} {self.serie.name} {self.name} ({self.start_production_year} - {self.end_production_year if self.end_production_year else "present"})'

    class Meta:
        verbose_name = "Car Trim"
        verbose_name_plural = "Car Trims"
        ordering = ['model', 'serie', 'start_production_year']
        
class CarSpecValue(models.Model):
    trim = models.ForeignKey(
        'CarTrim', 
        on_delete=models.CASCADE, 
        related_name='spec_values', 
        blank=False,  
        null=False    
    )
    spec = models.ForeignKey(
        'CarSpec',  
        on_delete=models.CASCADE, 
        related_name='values',  # Zmieniamy related_name na 'values'
        blank=False,  
        null=False    
    )
    value = models.CharField(
        max_length=255, 
        blank=False,  
        null=False    
    )
    unit = models.CharField(
        max_length=255, 
        blank=False,  
        null=False    
    )

    def __str__(self):
        return f'{self.trim} - {self.spec}'

    class Meta:
        verbose_name = "Car Spec Value"
        verbose_name_plural = "Car Spec Values"
        ordering = ['trim', 'spec']

class CarSpec(models.Model):
    spec_value = models.ForeignKey(
        'CarSpecValue', 
        on_delete=models.CASCADE, 
        related_name='spec_values',  # Zmieniamy related_name na 'spec_values'
        blank=False,  
        null=False    
    )
    name = models.CharField(
        max_length=255, 
        blank=False,  
        null=False    
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Car Spec"
        verbose_name_plural = "Car Specs"
        ordering = ['name']