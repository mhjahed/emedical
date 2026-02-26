# admin_tools/urls.py

from django.urls import path
from . import views

app_name = 'admin_tools'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('users/', views.user_management, name='user_management'),
    path('users/create-staff/', views.create_staff_user, name='create_staff_user'),
    path('users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('settings/', views.system_settings, name='system_settings'),
    path('audit-logs/', views.audit_logs, name='audit_logs'),
    path('notifications/', views.notifications_management, name='notifications_management'),
    path('reports/', views.reports, name='reports'),
    path('export/', views.export_data, name='export_data'),
]