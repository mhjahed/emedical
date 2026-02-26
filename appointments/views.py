# appointments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q

from .models import Appointment, AppointmentDocument, TimeSlot
from .forms import (
    AppointmentBookingForm, DoctorAppointmentForm, RescheduleForm,
    DocumentUploadForm, GenerateMeetLinkForm
)
from doctors.models import DoctorProfile
from accounts.decorators import patient_required, medical_staff_required


# ============ Patient Views ============

@login_required
def book_appointment(request):
    """Patient: Book new appointment"""
    doctors = DoctorProfile.objects.filter(is_active=True, is_accepting_appointments=True)
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, f'Appointment booked successfully! ID: {appointment.appointment_id}')
            return redirect('appointments:my_appointments')
    else:
        form = AppointmentBookingForm()
        # Pre-select doctor if specified
        doctor_id = request.GET.get('doctor')
        if doctor_id:
            form.fields['doctor'].initial = doctor_id
    
    return render(request, 'appointments/book_appointment.html', {
        'form': form,
        'doctors': doctors
    })


@login_required
def my_appointments(request):
    """Patient: View own appointments"""
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    paginator = Paginator(appointments, 10)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    
    return render(request, 'appointments/my_appointments.html', {
        'appointments': appointments,
        'status_filter': status_filter
    })


@login_required
def appointment_detail(request, appointment_id):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    # Check permission
    if appointment.patient != request.user and appointment.doctor.user != request.user:
        if not request.user.is_superadmin:
            messages.error(request, 'You do not have permission to view this appointment.')
            return redirect('core:home')
    
    documents = appointment.documents.all()
    
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment,
        'documents': documents
    })


@login_required
def cancel_appointment(request, appointment_id):
    """Patient: Cancel appointment"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id, patient=request.user)
    
    if appointment.status in ['completed', 'cancelled']:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('appointments:my_appointments')
    
    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, 'Appointment cancelled successfully.')
    return redirect('appointments:my_appointments')


# ============ Doctor Views ============

@medical_staff_required
def doctor_appointments(request):
    """Doctor: View appointments"""
    try:
        doctor = request.user.doctor_profile
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor profile not found.')
        return redirect('doctors:dashboard')
    
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-date', '-time')
    
    # Filters
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter:
        appointments = appointments.filter(date=date_filter)
    
    # Today's appointments
    today = timezone.now().date()
    today_appointments = Appointment.objects.filter(doctor=doctor, date=today).order_by('time')
    pending_count = Appointment.objects.filter(doctor=doctor, status='pending').count()
    
    paginator = Paginator(appointments, 15)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    
    return render(request, 'appointments/doctor_appointments.html', {
        'appointments': appointments,
        'today_appointments': today_appointments,
        'pending_count': pending_count,
        'status_filter': status_filter,
        'date_filter': date_filter
    })


@medical_staff_required
def update_appointment(request, appointment_id):
    """Doctor: Update appointment status and details"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    # Check permission
    if appointment.doctor.user != request.user and not request.user.is_superadmin:
        messages.error(request, 'Permission denied.')
        return redirect('doctors:dashboard')
    
    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointments:doctor_appointments')
    else:
        form = DoctorAppointmentForm(instance=appointment)
    
    document_form = DocumentUploadForm()
    
    return render(request, 'appointments/update_appointment.html', {
        'form': form,
        'appointment': appointment,
        'document_form': document_form
    })


@medical_staff_required
def accept_appointment(request, appointment_id):
    """Doctor: Accept appointment"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    if appointment.doctor.user != request.user and not request.user.is_superadmin:
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    appointment.status = 'confirmed'
    appointment.save()
    
    return JsonResponse({'success': True, 'message': 'Appointment confirmed'})


@medical_staff_required
def reject_appointment(request, appointment_id):
    """Doctor: Reject/Cancel appointment"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    if appointment.doctor.user != request.user and not request.user.is_superadmin:
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    appointment.status = 'cancelled'
    appointment.save()
    
    return JsonResponse({'success': True, 'message': 'Appointment cancelled'})


@medical_staff_required
def add_meet_link(request, appointment_id):
    """Doctor: Add Google Meet link"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    if appointment.doctor.user != request.user and not request.user.is_superadmin:
        messages.error(request, 'Permission denied.')
        return redirect('appointments:doctor_appointments')
    
    if request.method == 'POST':
        form = GenerateMeetLinkForm(request.POST)
        if form.is_valid():
            appointment.meet_link = form.cleaned_data['meet_link']
            appointment.meet_created_at = timezone.now()
            appointment.is_video_consultation = True
            appointment.save()
            messages.success(request, 'Google Meet link added successfully.')
            return redirect('appointments:update_appointment', appointment_id=appointment_id)
    else:
        form = GenerateMeetLinkForm()
    
    return render(request, 'appointments/add_meet_link.html', {
        'form': form,
        'appointment': appointment
    })


@medical_staff_required
def upload_document(request, appointment_id):
    """Upload document for appointment"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.appointment = appointment
            document.uploaded_by = request.user
            document.save()
            return JsonResponse({
                'success': True,
                'document_id': document.id,
                'title': document.title
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid form data'})


@medical_staff_required
def complete_appointment(request, appointment_id):
    """Doctor: Mark appointment as completed"""
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    
    if appointment.doctor.user != request.user and not request.user.is_superadmin:
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    appointment.status = 'completed'
    appointment.save()
    
    return JsonResponse({'success': True, 'message': 'Appointment marked as completed'})


# ============ AJAX Views ============

def get_doctor_slots(request, doctor_id):
    """Get available time slots for a doctor on a specific date"""
    date_str = request.GET.get('date')
    
    if not date_str:
        return JsonResponse({'slots': []})
    
    try:
        doctor = DoctorProfile.objects.get(id=doctor_id)
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Get all time slots
        all_slots = TimeSlot.objects.filter(is_active=True)
        
        # Get booked slots
        booked_times = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            status__in=['pending', 'confirmed']
        ).values_list('time', flat=True)
        
        available_slots = []
        for slot in all_slots:
            if slot.start_time not in booked_times:
                available_slots.append({
                    'id': slot.id,
                    'time': slot.start_time.strftime('%H:%M'),
                    'display': slot.__str__()
                })
        
        return JsonResponse({'slots': available_slots})
    
    except DoctorProfile.DoesNotExist:
        return JsonResponse({'slots': []})


def check_availability(request):
    """Check if a specific time slot is available"""
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    time = request.GET.get('time')
    
    if not all([doctor_id, date, time]):
        return JsonResponse({'available': False})
    
    exists = Appointment.objects.filter(
        doctor_id=doctor_id,
        date=date,
        time=time,
        status__in=['pending', 'confirmed']
    ).exists()
    
    return JsonResponse({'available': not exists})