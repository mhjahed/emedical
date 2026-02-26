# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .forms import (
    PatientSignUpForm, CustomLoginForm, DoctorLoginForm,
    UserProfileForm, PatientProfileForm, CustomPasswordChangeForm
)
from .models import ActivityLog, PatientProfile
from .decorators import role_required, patient_required, medical_staff_required

User = get_user_model()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_activity(user, action, description, request):
    ActivityLog.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )


def patient_signup(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            log_activity(user, 'create', 'Patient account created', request)
            messages.success(request, 'Account created successfully! Welcome to MediCare.')
            return redirect('accounts:profile')
    else:
        form = PatientSignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def patient_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            remember_me = form.cleaned_data.get('remember_me')
            
            if not remember_me:
                request.session.set_expiry(0)
            
            login(request, user)
            log_activity(user, 'login', 'User logged in', request)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            next_url = request.GET.get('next', 'core:home')
            return redirect(next_url)
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def doctor_login(request):
    if request.user.is_authenticated:
        if request.user.is_medical_staff:
            return redirect('doctors:dashboard')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = DoctorLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            log_activity(user, 'login', 'Doctor/Staff logged in', request)
            messages.success(request, f'Welcome back, Dr. {user.get_full_name()}!')
            return redirect('doctors:dashboard')
    else:
        form = DoctorLoginForm()
    
    return render(request, 'accounts/doctor_login.html', {'form': form})


@login_required
def user_logout(request):
    log_activity(request.user, 'logout', 'User logged out', request)
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')


@login_required
def profile(request):
    user = request.user
    patient_profile = None
    
    if user.is_patient:
        patient_profile, created = PatientProfile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'patient_profile': patient_profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    patient_profile = None
    patient_form = None
    
    if user.is_patient:
        patient_profile, created = PatientProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        
        if user.is_patient:
            patient_form = PatientProfileForm(request.POST, instance=patient_profile)
            if user_form.is_valid() and patient_form.is_valid():
                user_form.save()
                patient_form.save()
                log_activity(user, 'update', 'Profile updated', request)
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        else:
            if user_form.is_valid():
                user_form.save()
                log_activity(user, 'update', 'Profile updated', request)
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=user)
        if user.is_patient:
            patient_form = PatientProfileForm(instance=patient_profile)
    
    context = {
        'user_form': user_form,
        'patient_form': patient_form,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log_activity(user, 'update', 'Password changed', request)
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def activity_log(request):
    logs = ActivityLog.objects.filter(user=request.user)[:50]
    return render(request, 'accounts/activity_log.html', {'logs': logs})