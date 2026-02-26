# media_manager/urls.py

from django.urls import path
from . import views

app_name = 'media_manager'

urlpatterns = [
    # Media Library
    path('', views.media_library, name='library'),
    path('upload/', views.upload_file, name='upload'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('file/<int:file_id>/', views.file_details, name='file_details'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    
    # Galleries
    path('galleries/', views.gallery_list, name='gallery_list'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery_detail'),
    path('gallery/add/<int:gallery_id>/', views.add_to_gallery, name='add_to_gallery'),
    
    # Public
    path('view/<slug:slug>/', views.public_gallery, name='public_gallery'),
]