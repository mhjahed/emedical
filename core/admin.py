# core/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HospitalSettings, HeroSlide, AboutSection, Feature,
    Testimonial, FAQ, ContactMessage, StaticPage
)


@admin.register(HospitalSettings)
class HospitalSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'tagline', 'logo', 'favicon')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone', 'phone_secondary', 'emergency_phone')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code', 'country')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
        }),
        ('Map', {
            'fields': ('google_map_embed', 'latitude', 'longitude')
        }),
        ('Working Hours', {
            'fields': ('working_hours',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Footer', {
            'fields': ('footer_text', 'copyright_text')
        }),
    )
    
    def has_add_permission(self, request):
        return not HospitalSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'preview_image']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'subtitle']
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    preview_image.short_description = 'Preview'


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'years_experience', 'total_doctors', 'is_active']
    
    def has_add_permission(self, request):
        return not AboutSection.objects.exists()


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'content']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['question', 'answer']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'created_at')
        }),
        ('Admin Actions', {
            'fields': ('status', 'admin_notes')
        }),
    )


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'show_in_footer', 'is_active', 'order']
    list_filter = ['is_active', 'show_in_footer']
    list_editable = ['show_in_footer', 'is_active', 'order']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}