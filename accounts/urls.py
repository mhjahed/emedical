# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.patient_signup, name='signup'),
    path('login/', views.patient_login, name='login'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('activity-log/', views.activity_log, name='activity_log'),
]