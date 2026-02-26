# appointments/urls.py

from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # Patient URLs
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('detail/<str:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('cancel/<str:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    
    # Doctor URLs
    path('doctor/', views.doctor_appointments, name='doctor_appointments'),
    path('update/<str:appointment_id>/', views.update_appointment, name='update_appointment'),
    path('accept/<str:appointment_id>/', views.accept_appointment, name='accept_appointment'),
    path('reject/<str:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('complete/<str:appointment_id>/', views.complete_appointment, name='complete_appointment'),
    path('add-meet-link/<str:appointment_id>/', views.add_meet_link, name='add_meet_link'),
    path('upload-document/<str:appointment_id>/', views.upload_document, name='upload_document'),
    
    # AJAX URLs
    path('get-slots/<int:doctor_id>/', views.get_doctor_slots, name='get_doctor_slots'),
    path('check-availability/', views.check_availability, name='check_availability'),
]