# pdf_system/forms.py

from django import forms
from .models import PDFTemplate, GeneratedPDF, PatientDocument


class PDFTemplateForm(forms.ModelForm):
    class Meta:
        model = PDFTemplate
        fields = [
            'name', 'slug', 'template_type', 'description',
            'header_content', 'body_content', 'footer_content',
            'header_image', 'footer_image', 'logo',
            'page_size', 'orientation',
            'margin_top', 'margin_bottom', 'margin_left', 'margin_right',
            'dynamic_fields', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'template_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'page_size': forms.Select(attrs={'class': 'form-select'}),
            'orientation': forms.Select(attrs={'class': 'form-select'}),
            'margin_top': forms.NumberInput(attrs={'class': 'form-control'}),
            'margin_bottom': forms.NumberInput(attrs={'class': 'form-control'}),
            'margin_left': forms.NumberInput(attrs={'class': 'form-control'}),
            'margin_right': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DynamicPDFForm(forms.Form):
    """Dynamically generated form based on template fields"""
    
    def __init__(self, template, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add fields based on template's dynamic_fields
        for field_def in template.dynamic_fields:
            field_name = field_def.get('name')
            field_label = field_def.get('label', field_name)
            field_type = field_def.get('type', 'text')
            required = field_def.get('required', False)
            
            if field_type == 'text':
                self.fields[field_name] = forms.CharField(
                    label=field_label,
                    required=required,
                    widget=forms.TextInput(attrs={'class': 'form-control'})
                )
            elif field_type == 'textarea':
                self.fields[field_name] = forms.CharField(
                    label=field_label,
                    required=required,
                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
                )
            elif field_type == 'date':
                self.fields[field_name] = forms.DateField(
                    label=field_label,
                    required=required,
                    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
                )
            elif field_type == 'number':
                self.fields[field_name] = forms.IntegerField(
                    label=field_label,
                    required=required,
                    widget=forms.NumberInput(attrs={'class': 'form-control'})
                )
            elif field_type == 'select':
                choices = [(c, c) for c in field_def.get('choices', [])]
                self.fields[field_name] = forms.ChoiceField(
                    label=field_label,
                    required=required,
                    choices=choices,
                    widget=forms.Select(attrs={'class': 'form-select'})
                )


class PatientSelectForm(forms.Form):
    """Form to select a patient for PDF generation"""
    patient = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select Patient'
    )
    
    def __init__(self, *args, **kwargs):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = User.objects.filter(role='patient', is_active=True)


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = PatientDocument
        fields = ['document_type', 'title', 'description', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }