# media_manager/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import MediaFolder, MediaFile, Gallery, GalleryImage


@admin.register(MediaFolder)
class MediaFolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_type', 'folder', 'file_size_display', 'preview', 'uploaded_by', 'created_at']
    list_filter = ['file_type', 'folder', 'created_at']
    search_fields = ['title', 'description']
    
    def preview(self, obj):
        if obj.is_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.file.url)
        return obj.file_type
    preview.short_description = 'Preview'


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryImageInline]