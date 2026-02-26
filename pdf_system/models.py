# pdf_system/models.py

from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
import uuid


class PDFTemplate(models.Model):
    """PDF templates created by superadmin"""
    TEMPLATE_TYPE_CHOICES = (
        ('prescription', 'Prescription'),
        ('medical_report', 'Medical Report'),
        ('discharge_summary', 'Discharge Summary'),
        ('lab_report', 'Lab Report'),
        ('certificate', 'Medical Certificate'),
        ('invoice', 'Invoice'),
        ('referral', 'Referral Letter'),
        ('consent_form', 'Consent Form'),
        ('custom', 'Custom'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    # Template content with placeholders
    # Placeholders: {{patient_name}}, {{patient_age}}, {{doctor_name}}, {{date}}, etc.
    header_content = RichTextField(blank=True, null=True, help_text='Header section of PDF')
    body_content = RichTextField(help_text='Main content with placeholders like {{patient_name}}')
    footer_content = RichTextField(blank=True, null=True, help_text='Footer section of PDF')
    
    # Styling
    header_image = models.ImageField(upload_to='pdf_templates/headers/', blank=True, null=True)
    footer_image = models.ImageField(upload_to='pdf_templates/footers/', blank=True, null=True)
    logo = models.ImageField(upload_to='pdf_templates/logos/', blank=True, null=True)
    
    # Page settings
    page_size = models.CharField(max_length=20, default='A4', choices=[
        ('A4', 'A4'),
        ('Letter', 'Letter'),
        ('Legal', 'Legal'),
    ])
    orientation = models.CharField(max_length=20, default='portrait', choices=[
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ])
    margin_top = models.PositiveIntegerField(default=50)
    margin_bottom = models.PositiveIntegerField(default=50)
    margin_left = models.PositiveIntegerField(default=50)
    margin_right = models.PositiveIntegerField(default=50)
    
    # Dynamic fields definition (JSON)
    # Format: [{"name": "diagnosis", "label": "Diagnosis", "type": "text", "required": true}, ...]
    dynamic_fields = models.JSONField(default=list, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_templates'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

    def get_placeholders(self):
        """Extract placeholders from template content"""
        import re
        content = f"{self.header_content or ''} {self.body_content} {self.footer_content or ''}"
        placeholders = re.findall(r'\{\{(\w+)\}\}', content)
        return list(set(placeholders))


class GeneratedPDF(models.Model):
    """PDFs generated from templates"""
    pdf_id = models.CharField(max_length=20, unique=True, editable=False)
    template = models.ForeignKey(PDFTemplate, on_delete=models.SET_NULL, null=True, related_name='generated_pdfs')
    
    # Ownership
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='generated_pdfs'
    )
    generated_for = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_pdfs',
        blank=True,
        null=True
    )
    
    # Related appointment (optional)
    appointment = models.ForeignKey(
        'appointments.Appointment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_pdfs'
    )
    
    # Filled data (JSON)
    filled_data = models.JSONField(default=dict)
    
    # Generated file
    pdf_file = models.FileField(upload_to='generated_pdfs/')
    file_name = models.CharField(max_length=255)
    
    # Metadata
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Generated PDF'
        verbose_name_plural = 'Generated PDFs'

    def __str__(self):
        return f"{self.title} ({self.pdf_id})"

    def save(self, *args, **kwargs):
        if not self.pdf_id:
            self.pdf_id = f"PDF-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class PatientDocument(models.Model):
    """Documents uploaded by/for patients"""
    DOCUMENT_TYPE_CHOICES = (
        ('prescription', 'Prescription'),
        ('report', 'Medical Report'),
        ('lab_result', 'Lab Result'),
        ('imaging', 'Imaging/X-Ray'),
        ('insurance', 'Insurance Document'),
        ('id_proof', 'ID Proof'),
        ('other', 'Other'),
    )

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_documents'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents'
    )
    
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='patient_documents/')
    
    # Related to generated PDF
    generated_pdf = models.ForeignKey(
        GeneratedPDF,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.patient.get_full_name()}"