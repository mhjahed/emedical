# news/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Article, ArticleImage, Comment


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'is_home_featured', 'views', 'published_at']
    list_filter = ['status', 'is_featured', 'is_home_featured', 'category', 'created_at']
    list_editable = ['status', 'is_featured', 'is_home_featured']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    
    inlines = [ArticleImageInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'subtitle', 'excerpt', 'author')
        }),
        ('Content', {
            'fields': ('content', 'primary_image', 'primary_image_caption')
        }),
        ('Organization', {
            'fields': ('category', 'tags')
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'is_home_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['user__email', 'content']