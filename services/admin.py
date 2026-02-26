# services/admin.py

from django.contrib import admin
from .models import ServiceCategory, Service, ServiceImage, ServiceFAQ


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1


class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active', 'is_featured', 'order']
    list_filter = ['is_active', 'is_featured', 'category']
    list_editable = ['is_active', 'is_featured', 'order']
    search_fields = ['name', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['related_doctors']
    
    inlines = [ServiceImageInline, ServiceFAQInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'category', 'short_description')
        }),
        ('Content', {
            'fields': ('full_description', 'image', 'icon')
        }),
        ('Pricing', {
            'fields': ('price', 'price_note')
        }),
        ('Related', {
            'fields': ('related_doctors',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )