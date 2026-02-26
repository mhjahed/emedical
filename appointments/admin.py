# appointments/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import TimeSlot, Appointment, AppointmentDocument, AppointmentReminder


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']


class AppointmentDocumentInline(admin.TabularInline):
    model = AppointmentDocument
    extra = 0
    readonly_fields = ['uploaded_by', 'uploaded_at']


class AppointmentReminderInline(admin.TabularInline):
    model = AppointmentReminder
    extra = 0


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'appointment_id', 'patient_name', 'doctor_name', 'date', 'time',
        'appointment_type', 'status', 'is_video_consultation', 'meet_link_status'
    ]
    list_filter = ['status', 'appointment_type', 'is_video_consultation', 'date', 'created_at']
    search_fields = ['appointment_id', 'patient__email', 'patient__first_name', 'doctor__user__first_name']
    date_hierarchy = 'date'
    readonly_fields = ['appointment_id', 'created_at', 'updated_at', 'confirmed_at', 'completed_at']
    
    inlines = [AppointmentDocumentInline, AppointmentReminderInline]
    
    fieldsets = (
        ('Appointment Info', {
            'fields': ('appointment_id', 'patient', 'doctor', 'date', 'time', 'appointment_type')
        }),
        ('Details', {
            'fields': ('reason', 'symptoms', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'fee', 'is_paid')
        }),
        ('Video Consultation', {
            'fields': ('is_video_consultation', 'meet_link', 'meet_created_at')
        }),
        ('Doctor Notes', {
            'fields': ('doctor_notes', 'diagnosis', 'prescription', 'follow_up_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def patient_name(self, obj):
        return obj.patient.get_full_name()
    patient_name.short_description = 'Patient'
    
    def doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    doctor_name.short_description = 'Doctor'
    
    def meet_link_status(self, obj):
        if obj.meet_link:
            return format_html('<span style="color: green;">✓ Added</span>')
        return format_html('<span style="color: gray;">-</span>')
    meet_link_status.short_description = 'Meet Link'


@admin.register(AppointmentDocument)
class AppointmentDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'appointment', 'document_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['title', 'appointment__appointment_id']