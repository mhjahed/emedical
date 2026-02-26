# doctors/urls.py

from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Public Pages
    path('', views.doctors_list, name='doctors_list'),
    path('doctor/<slug:slug>/', views.doctor_detail, name='doctor_detail'),
    path('staff/', views.staff_list, name='staff_list'),
    
    # Dashboard (Private)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-appointments/', views.doctor_appointments, name='appointments'),
    path('download-id-card/', views.download_id_card, name='download_id_card'),
    
    # Admin Actions
    path('generate-id-card/<int:user_id>/', views.generate_staff_id_card, name='generate_id_card'),
    
    # Barcode Scanner System
    path('scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('verify-barcode/', views.verify_barcode, name='verify_barcode'),
    path('manual-barcode/', views.manual_barcode_entry, name='manual_barcode'),
]