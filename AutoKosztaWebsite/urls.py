"""
URL configuration for AutoKosztaWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from Car_Management.views import home_page, calculators, car_selection_view, load_models, load_generations, load_series, load_trims, load_specs


urlpatterns = [
    path('admin/', admin.site.urls, name='admin_panel'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', home_page, name='home_page'),
    path('calculators/', calculators, name='calculators'),
    path('cars_base/', car_selection_view, name='cars_base'),
    path('ajax/load-models/', load_models, name='ajax_load_models'),
    path('ajax/load-generations/', load_generations, name='ajax_load_generations'),
    path('ajax/load-series/', load_series, name='ajax_load_series'),
    path('ajax/load-trims/', load_trims, name='ajax_load_trims'),
    path('ajax/load-specs/', load_specs, name='ajax_load_specs'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)