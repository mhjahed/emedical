# doctors/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Department, Specialization, DoctorProfile, StaffProfile,
    DoctorEducation, DoctorExperience, DoctorAward
)
from .utils import generate_id_card, generate_barcode


class DoctorEducationInline(admin.TabularInline):
    model = DoctorEducation
    extra = 1


class DoctorExperienceInline(admin.TabularInline):
    model = DoctorExperience
    extra = 1


class DoctorAwardInline(admin.TabularInline):
    model = DoctorAward
    extra = 1


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'is_active']
    list_filter = ['department', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'medi_id', 'department', 'designation', 'is_active', 'is_featured', 'id_card_preview']
    list_filter = ['department', 'is_active', 'is_featured', 'is_accepting_appointments']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__medi_id']
    prepopulated_fields = {'slug': ('user',)}
    filter_horizontal = ['specializations']
    
    inlines = [DoctorEducationInline, DoctorExperienceInline, DoctorAwardInline]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'slug', 'department', 'specializations')
        }),
        ('Professional Details', {
            'fields': ('designation', 'qualifications', 'experience_years', 'license_number')
        }),
        ('Bio', {
            'fields': ('short_bio', 'full_bio')
        }),
        ('Contact', {
            'fields': ('consultation_email', 'consultation_phone')
        }),
        ('Fees', {
            'fields': ('consultation_fee', 'follow_up_fee')
        }),
        ('Availability', {
            'fields': ('available_days', 'start_time', 'end_time', 'slot_duration', 'max_patients_per_day')
        }),
        ('ID Card', {
            'fields': ('id_card_image', 'barcode_image')
        }),
        ('Social Media', {
            'fields': ('linkedin', 'twitter', 'facebook')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_accepting_appointments')
        }),
    )
    
    actions = ['generate_id_cards']
    
    def id_card_preview(self, obj):
        if obj.id_card_image:
            return format_html('<img src="{}" width="50" />', obj.id_card_image.url)
        return "No ID Card"
    id_card_preview.short_description = 'ID Card'
    
    def generate_id_cards(self, request, queryset):
        for profile in queryset:
            user = profile.user
            # Generate barcode
            barcode_content = generate_barcode(user.medi_id)
            if barcode_content:
                profile.barcode_image.save(f'barcode_{user.medi_id}.png', barcode_content)
            
            # Generate ID card
            id_card = generate_id_card(user, profile)
            if id_card:
                profile.id_card_image.save(f'id_card_{user.medi_id}.png', id_card)
                profile.save()
        
        self.message_user(request, f"ID cards generated for {queryset.count()} doctors.")
    generate_id_cards.short_description = "Generate ID Cards"


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'staff_type', 'department', 'is_active']
    list_filter = ['staff_type', 'department', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    actions = ['generate_id_cards']
    
    def generate_id_cards(self, request, queryset):
        for profile in queryset:
            user = profile.user
            barcode_content = generate_barcode(user.medi_id)
            if barcode_content:
                profile.barcode_image.save(f'barcode_{user.medi_id}.png', barcode_content)
            
            id_card = generate_id_card(user, profile)
            if id_card:
                profile.id_card_image.save(f'id_card_{user.medi_id}.png', id_card)
                profile.save()
        
        self.message_user(request, f"ID cards generated for {queryset.count()} staff members.")
    generate_id_cards.short_description = "Generate ID Cards"