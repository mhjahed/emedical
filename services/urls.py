# services/urls.py

from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_list, name='services_list'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),
    path('category/<slug:slug>/', views.category_services, name='category_services'),
]