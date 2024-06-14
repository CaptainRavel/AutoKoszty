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
from Car_Management.views import home_page, t_o_u, user_account, delete_account, calculators, car_selection_view, load_models, load_generations, load_series, load_trims, load_specs, login_view, logout_view, register, cars_list, add_car, edit_car, delete_car, get_car_data, user_reports, reports_list, add_report, edit_report, delete_report, get_report_data, priv_pol, generate_summary_xlsx, generate_summary_csv


urlpatterns = [
    path('', home_page, name='home_page'),
    path('admin/', admin.site.urls, name='admin_panel'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('home/', home_page, name='home_page'),
    path('privacy_policy/', priv_pol, name='priv_pol'),
    path('terms_of_use/', t_o_u, name='terms'),
    path('calculators/', calculators, name='calculators'),
    path('cars_base/', car_selection_view, name='cars_base'),
    path('user_account/', user_account, name='user_account'),
    path('delete_account/', delete_account, name='delete_account'),
    path('ajax/load-models/', load_models, name='ajax_load_models'),
    path('ajax/load-generations/', load_generations, name='ajax_load_generations'),
    path('ajax/load-series/', load_series, name='ajax_load_series'),
    path('ajax/load-trims/', load_trims, name='ajax_load_trims'),
    path('ajax/load-specs/', load_specs, name='ajax_load_specs'),
    path('cars/', cars_list, name='cars_list'),
    path('add/', add_car, name='add_car'),
    path('edit/<int:car_id>/', edit_car, name='edit_car'),
    path('delete/<int:car_id>/', delete_car, name='delete_car'),
    path('get_car_data/', get_car_data, name='get_car_data'),
    path('user_reports/', user_reports, name='user_reports'),
    path('reports/<int:car_id>/', reports_list, name='reports_list'),
    path('reports/add/<int:car_id>/', add_report, name='add_report'),
    path('reports/edit/<int:report_id>/<int:car_id>/', edit_report, name='edit_report'),
    path('reports/delete/<int:report_id>/<int:car_id>/', delete_report, name='delete_report'),
    path('get_report_data/', get_report_data, name='get_report_data'),
    path('generate_summary_xlsx/<int:car_id>/', generate_summary_xlsx, name='generate_summary_xlsx'),
    path('generate_summary_csv/<int:car_id>/', generate_summary_csv, name='generate_summary_csv'),
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
