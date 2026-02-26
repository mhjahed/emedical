# doctors/models.py

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
import uuid


class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text='Font Awesome icon class')
    image = models.ImageField(upload_to='departments/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Specialization(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='specializations')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DoctorProfile(models.Model):
    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    slug = models.SlugField(unique=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='doctors'
    )
    specializations = models.ManyToManyField(Specialization, blank=True)
    
    # Professional Info
    designation = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Bio
    short_bio = models.TextField(max_length=500, blank=True, null=True)
    full_bio = RichTextUploadingField(blank=True, null=True)
    
    # Contact
    consultation_email = models.EmailField(blank=True, null=True)
    consultation_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Fees
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    follow_up_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Availability
    available_days = models.JSONField(default=list, blank=True)  # Store as list of days
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    slot_duration = models.PositiveIntegerField(default=30, help_text='In minutes')
    max_patients_per_day = models.PositiveIntegerField(default=20)
    
    # ID Card
    id_card_image = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    
    # Social Media
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_accepting_appointments = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.user.first_name}-{self.user.last_name}")
            slug = base_slug
            counter = 1
            while DoctorProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"Dr. {self.user.get_full_name()}"

    @property
    def medi_id(self):
        return self.user.medi_id


class StaffProfile(models.Model):
    STAFF_TYPE_CHOICES = (
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('lab_technician', 'Lab Technician'),
        ('pharmacist', 'Pharmacist'),
        ('admin_staff', 'Administrative Staff'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    staff_type = models.CharField(max_length=50, choices=STAFF_TYPE_CHOICES)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff'
    )
    designation = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    
    # ID Card
    id_card_image = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_staff_type_display()})"

    @property
    def medi_id(self):
        return self.user.medi_id


class DoctorEducation(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class DoctorExperience(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='experiences')
    position = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.position} at {self.hospital}"


class DoctorAward(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True, null=True)
    year = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return self.title