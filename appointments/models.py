# appointments/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class TimeSlot(models.Model):
    """Pre-defined time slots"""
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_time']
        unique_together = ['start_time', 'end_time']

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rescheduled', 'Rescheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    APPOINTMENT_TYPE_CHOICES = (
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('checkup', 'Regular Checkup'),
        ('video_call', 'Video Consultation'),
    )

    # Unique ID
    appointment_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Parties
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )
    doctor = models.ForeignKey(
        'doctors.DoctorProfile',
        on_delete=models.CASCADE,
        related_name='doctor_appointments'
    )
    
    # Appointment Details
    date = models.DateField()
    time = models.TimeField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True)
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    
    # Description
    reason = models.TextField(help_text='Reason for appointment')
    symptoms = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text='Additional notes from patient')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Video Call (Google Meet)
    is_video_consultation = models.BooleanField(default=False)
    meet_link = models.URLField(blank=True, null=True, help_text='Google Meet link')
    meet_created_at = models.DateTimeField(blank=True, null=True)
    
    # Doctor Notes (after appointment)
    doctor_notes = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    
    # Fees
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.appointment_id} - {self.patient.get_full_name()} with Dr. {self.doctor.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = f"APT-{uuid.uuid4().hex[:8].upper()}"
        
        # Update timestamps
        if self.status == 'confirmed' and not self.confirmed_at:
            self.confirmed_at = timezone.now()
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        now = timezone.now()
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        return appointment_datetime > now

    @property
    def can_join_meeting(self):
        """Check if the meeting can be joined (within 15 minutes before and during)"""
        if not self.meet_link:
            return False
        
        now = timezone.now()
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        
        # Allow joining 15 minutes before
        start_window = appointment_datetime - timezone.timedelta(minutes=15)
        # Allow for 1 hour after start
        end_window = appointment_datetime + timezone.timedelta(hours=1)
        
        return start_window <= now <= end_window


class AppointmentDocument(models.Model):
    """Documents uploaded during/after appointment"""
    DOCUMENT_TYPE_CHOICES = (
        ('report', 'Medical Report'),
        ('prescription', 'Prescription'),
        ('lab_result', 'Lab Result'),
        ('image', 'Medical Image'),
        ('other', 'Other'),
    )

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='documents')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='appointments/documents/')
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.appointment.appointment_id}"


class AppointmentReminder(models.Model):
    """Appointment reminders"""
    REMINDER_TYPE_CHOICES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    )

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES)
    scheduled_for = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_for']

    def __str__(self):
        return f"Reminder for {self.appointment.appointment_id}"