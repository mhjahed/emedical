# pdf_system/admin.py

from django.contrib import admin
from .models import PDFTemplate, GeneratedPDF, PatientDocument


@admin.register(PDFTemplate)
class PDFTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'page_size', 'is_active', 'created_by', 'created_at']
    list_filter = ['template_type', 'is_active', 'page_size']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'template_type', 'description')
        }),
        ('Content', {
            'fields': ('header_content', 'body_content', 'footer_content')
        }),
        ('Images', {
            'fields': ('logo', 'header_image', 'footer_image')
        }),
        ('Page Settings', {
            'fields': ('page_size', 'orientation', 'margin_top', 'margin_bottom', 'margin_left', 'margin_right')
        }),
        ('Dynamic Fields', {
            'fields': ('dynamic_fields',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
    )


@admin.register(GeneratedPDF)
class GeneratedPDFAdmin(admin.ModelAdmin):
    list_display = ['pdf_id', 'title', 'template', 'generated_by', 'generated_for', 'created_at']
    list_filter = ['template', 'created_at']
    search_fields = ['pdf_id', 'title', 'generated_by__email', 'generated_for__email']
    readonly_fields = ['pdf_id', 'created_at']


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'patient', 'document_type', 'uploaded_by', 'created_at']
    list_filter = ['document_type', 'created_at']
    search_fields = ['title', 'patient__email']