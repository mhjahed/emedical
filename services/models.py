# services/models.py

from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='services/categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Service Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name='services')
    
    # Content
    short_description = models.TextField(max_length=500)
    full_description = RichTextUploadingField()
    
    # Media
    image = models.ImageField(upload_to='services/')
    icon = models.CharField(max_length=50, blank=True, null=True, help_text='Font Awesome icon class')
    
    # Pricing (optional)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_note = models.CharField(max_length=100, blank=True, null=True, help_text='e.g., "Starting from" or "Per session"')
    
    # Related doctors - using string reference to avoid circular import
    related_doctors = models.ManyToManyField('doctors.DoctorProfile', blank=True, related_name='services')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceImage(models.Model):
    """Additional images for service gallery"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='services/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.name} - Image {self.order}"


class ServiceFAQ(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service FAQ'
        verbose_name_plural = 'Service FAQs'

    def __str__(self):
        return self.question