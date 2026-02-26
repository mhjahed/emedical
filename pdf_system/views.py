# pdf_system/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.paginator import Paginator

from .models import PDFTemplate, GeneratedPDF, PatientDocument
from .forms import PDFTemplateForm, DynamicPDFForm, PatientSelectForm, DocumentUploadForm
from .utils import generate_pdf_from_template
from accounts.decorators import superadmin_required, medical_staff_required


# ============ Template Management (Superadmin) ============

@superadmin_required
def template_list(request):
    """List all PDF templates"""
    templates = PDFTemplate.objects.all()
    return render(request, 'pdf_system/template_list.html', {'templates': templates})


@superadmin_required
def create_template(request):
    """Create new PDF template"""
    if request.method == 'POST':
        form = PDFTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.save()
            messages.success(request, 'Template created successfully!')
            return redirect('pdf_system:template_list')
    else:
        form = PDFTemplateForm()
    
    return render(request, 'pdf_system/create_template.html', {'form': form})


@superadmin_required
def edit_template(request, slug):
    """Edit PDF template"""
    template = get_object_or_404(PDFTemplate, slug=slug)
    
    if request.method == 'POST':
        form = PDFTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Template updated successfully!')
            return redirect('pdf_system:template_list')
    else:
        form = PDFTemplateForm(instance=template)
    
    return render(request, 'pdf_system/edit_template.html', {
        'form': form,
        'template': template
    })


@superadmin_required
def delete_template(request, slug):
    """Delete PDF template"""
    template = get_object_or_404(PDFTemplate, slug=slug)
    template.delete()
    messages.success(request, 'Template deleted successfully!')
    return redirect('pdf_system:template_list')


@superadmin_required
def preview_template(request, slug):
    """Preview PDF template"""
    template = get_object_or_404(PDFTemplate, slug=slug)
    
    # Generate preview with sample data
    sample_data = {
        'patient_name': 'John Doe',
        'patient_age': '35',
        'patient_gender': 'Male',
        'doctor_name': 'Dr. Jane Smith',
        'diagnosis': 'Sample diagnosis for preview',
        'prescription': 'Sample prescription content',
    }
    
    pdf_file = generate_pdf_from_template(template, sample_data)
    
    if pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="preview_{template.slug}.pdf"'
        return response
    
    messages.error(request, 'Failed to generate preview.')
    return redirect('pdf_system:template_list')


# ============ PDF Generation (Doctors/Staff) ============

@medical_staff_required
def generate_pdf(request, template_slug):
    """Generate PDF from template"""
    template = get_object_or_404(PDFTemplate, slug=template_slug, is_active=True)
    
    if request.method == 'POST':
        patient_form = PatientSelectForm(request.POST)
        dynamic_form = DynamicPDFForm(template, request.POST)
        
        if patient_form.is_valid() and dynamic_form.is_valid():
            patient = patient_form.cleaned_data['patient']
            filled_data = dynamic_form.cleaned_data
            
            # Get doctor profile if user is doctor
            doctor = None
            if request.user.is_doctor:
                doctor = getattr(request.user, 'doctor_profile', None)
            
            # Generate PDF
            pdf_file = generate_pdf_from_template(template, filled_data, patient, doctor)
            
            if pdf_file:
                # Save generated PDF
                generated_pdf = GeneratedPDF.objects.create(
                    template=template,
                    generated_by=request.user,
                    generated_for=patient,
                    filled_data=filled_data,
                    title=f"{template.name} - {patient.get_full_name()}",
                )
                generated_pdf.pdf_file.save(pdf_file.name, pdf_file)
                generated_pdf.file_name = pdf_file.name
                generated_pdf.save()
                
                messages.success(request, f'PDF generated successfully! ID: {generated_pdf.pdf_id}')
                return redirect('pdf_system:view_generated_pdf', pdf_id=generated_pdf.pdf_id)
            else:
                messages.error(request, 'Failed to generate PDF.')
    else:
        patient_form = PatientSelectForm()
        dynamic_form = DynamicPDFForm(template)
        
        # Pre-fill patient if specified
        patient_id = request.GET.get('patient')
        if patient_id:
            patient_form.fields['patient'].initial = patient_id
    
    return render(request, 'pdf_system/generate_pdf.html', {
        'template': template,
        'patient_form': patient_form,
        'dynamic_form': dynamic_form
    })


@medical_staff_required
def select_template(request):
    """Select template for PDF generation"""
    templates = PDFTemplate.objects.filter(is_active=True)
    return render(request, 'pdf_system/select_template.html', {'templates': templates})


@medical_staff_required
def my_generated_pdfs(request):
    """View PDFs generated by current user"""
    pdfs = GeneratedPDF.objects.filter(generated_by=request.user)
    
    paginator = Paginator(pdfs, 20)
    page = request.GET.get('page')
    pdfs = paginator.get_page(page)
    
    return render(request, 'pdf_system/my_generated_pdfs.html', {'pdfs': pdfs})


# ============ Patient Views ============

@login_required
def my_documents(request):
    """Patient: View own documents and generated PDFs"""
    documents = PatientDocument.objects.filter(patient=request.user)
    received_pdfs = GeneratedPDF.objects.filter(generated_for=request.user)
    
    return render(request, 'pdf_system/my_documents.html', {
        'documents': documents,
        'received_pdfs': received_pdfs
    })


@login_required
def view_generated_pdf(request, pdf_id):
    """View generated PDF"""
    pdf = get_object_or_404(GeneratedPDF, pdf_id=pdf_id)
    
    # Check permission
    if pdf.generated_for != request.user and pdf.generated_by != request.user:
        if not request.user.is_superadmin:
            messages.error(request, 'Permission denied.')
            return redirect('core:home')
    
    return render(request, 'pdf_system/view_pdf.html', {'pdf': pdf})


@login_required
def download_pdf(request, pdf_id):
    """Download generated PDF"""
    pdf = get_object_or_404(GeneratedPDF, pdf_id=pdf_id)
    
    # Check permission
    if pdf.generated_for != request.user and pdf.generated_by != request.user:
        if not request.user.is_superadmin:
            messages.error(request, 'Permission denied.')
            return redirect('core:home')
    
    response = FileResponse(pdf.pdf_file.open(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf.file_name}"'
    return response