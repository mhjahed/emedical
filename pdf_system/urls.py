# pdf_system/urls.py

from django.urls import path
from . import views

app_name = 'pdf_system'

urlpatterns = [
    # Template Management (Superadmin)
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.create_template, name='create_template'),
    path('templates/edit/<slug:slug>/', views.edit_template, name='edit_template'),
    path('templates/delete/<slug:slug>/', views.delete_template, name='delete_template'),
    path('templates/preview/<slug:slug>/', views.preview_template, name='preview_template'),
    
    # PDF Generation (Doctors/Staff)
    path('select-template/', views.select_template, name='select_template'),
    path('generate/<slug:template_slug>/', views.generate_pdf, name='generate_pdf'),
    path('my-pdfs/', views.my_generated_pdfs, name='my_generated_pdfs'),
    
    # Patient Views
    path('my-documents/', views.my_documents, name='my_documents'),
    path('view/<str:pdf_id>/', views.view_generated_pdf, name='view_generated_pdf'),
    path('download/<str:pdf_id>/', views.download_pdf, name='download_pdf'),
]