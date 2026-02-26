# news/urls.py

from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Public
    path('', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('category/<slug:slug>/', views.category_articles, name='category_articles'),
    path('tag/<slug:slug>/', views.tag_articles, name='tag_articles'),
    
    # Doctor/Staff Management
    path('my-articles/', views.my_articles, name='my_articles'),
    path('create/', views.create_article, name='create_article'),
    path('edit/<slug:slug>/', views.edit_article, name='edit_article'),
    path('delete/<slug:slug>/', views.delete_article, name='delete_article'),
    path('add-image/<slug:slug>/', views.add_gallery_image, name='add_gallery_image'),
    path('delete-image/<int:image_id>/', views.delete_gallery_image, name='delete_gallery_image'),
]