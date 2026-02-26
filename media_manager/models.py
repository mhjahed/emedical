# media_manager/models.py

from django.db import models
from django.conf import settings
import os
import uuid


def get_upload_path(instance, filename):
    """Generate upload path based on folder"""
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    if instance.folder:
        return f"media_library/{instance.folder.slug}/{new_filename}"
    return f"media_library/uncategorized/{new_filename}"


class MediaFolder(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def full_path(self):
        if self.parent:
            return f"{self.parent.full_path}/{self.name}"
        return self.name


class MediaFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('image', 'Image'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=get_upload_path)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='image')
    folder = models.ForeignKey(MediaFolder, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    
    # Metadata
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file_size = models.PositiveIntegerField(default=0)  # In bytes
    
    # Image specific
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    
    # Tracking
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            
            # Detect file type
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                self.file_type = 'image'
            elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt']:
                self.file_type = 'document'
            elif ext in ['.mp4', '.avi', '.mov', '.wmv']:
                self.file_type = 'video'
            elif ext in ['.mp3', '.wav', '.ogg']:
                self.file_type = 'audio'
            else:
                self.file_type = 'other'
            
            # Get image dimensions
            if self.file_type == 'image':
                try:
                    from PIL import Image
                    img = Image.open(self.file)
                    self.width, self.height = img.size
                except:
                    pass
        
        super().save(*args, **kwargs)

    @property
    def file_size_display(self):
        """Human readable file size"""
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    @property
    def is_image(self):
        return self.file_type == 'image'


class Gallery(models.Model):
    """Image galleries for various sections"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL, null=True, blank=True, related_name='cover_for_galleries')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Galleries'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.gallery.name} - {self.image.title}"