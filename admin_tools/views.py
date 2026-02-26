# admin_tools/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import SystemSetting, Notification, AuditLog, BackupLog
from accounts.models import User, ActivityLog
from appointments.models import Appointment
from news.models import Article
from doctors.models import DoctorProfile
from accounts.decorators import superadmin_required


@superadmin_required
def admin_dashboard(request):
    """Main admin dashboard"""
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    # Statistics
    stats = {
        'total_users': User.objects.count(),
        'total_patients': User.objects.filter(role='patient').count(),
        'total_doctors': User.objects.filter(role='doctor').count(),
        'total_staff': User.objects.filter(role='staff').count(),
        'new_users_30_days': User.objects.filter(created_at__gte=thirty_days_ago).count(),
        
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'today_appointments': Appointment.objects.filter(date=today).count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
        
        'total_articles': Article.objects.count(),
        'published_articles': Article.objects.filter(status='published').count(),
    }
    
    # Recent activity
    recent_activity = ActivityLog.objects.all()[:10]
    
    # Recent appointments
    recent_appointments = Appointment.objects.all()[:10]
    
    # Pending items
    pending_appointments = Appointment.objects.filter(status='pending')[:5]
    
    context = {
        'stats': stats,
        'recent_activity': recent_activity,
        'recent_appointments': recent_appointments,
        'pending_appointments': pending_appointments,
    }
    return render(request, 'admin_tools/dashboard.html', context)


@superadmin_required
def user_management(request):
    """User management page"""
    users = User.objects.all().order_by('-created_at')
    
    # Filters
    role_filter = request.GET.get('role', '')
    search = request.GET.get('search', '')
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    if search:
        users = users.filter(
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(medi_id__icontains=search)
        )
    
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    return render(request, 'admin_tools/user_management.html', {
        'users': users,
        'role_filter': role_filter,
        'search': search
    })


@superadmin_required
def create_staff_user(request):
    """Create doctor or staff user"""
    from accounts.forms import UserProfileForm
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        
        if role not in ['doctor', 'staff']:
            messages.error(request, 'Invalid role selected.')
            return redirect('admin_tools:create_staff_user')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('admin_tools:create_staff_user')
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True
        )
        
        # Create profile
        if role == 'doctor':
            from doctors.models import DoctorProfile
            DoctorProfile.objects.create(user=user)
        else:
            from doctors.models import StaffProfile
            StaffProfile.objects.create(user=user, staff_type='other')
        
        messages.success(request, f'{role.title()} account created successfully!')
        return redirect('admin_tools:user_management')
    
    return render(request, 'admin_tools/create_staff_user.html')


@superadmin_required
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    
    if user.is_superadmin:
        return JsonResponse({'success': False, 'message': 'Cannot modify superadmin'})
    
    user.is_active = not user.is_active
    user.save()
    
    return JsonResponse({
        'success': True,
        'is_active': user.is_active,
        'message': f'User {"activated" if user.is_active else "deactivated"}'
    })


@superadmin_required
def system_settings(request):
    """System settings page"""
    settings = SystemSetting.objects.all()
    
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('setting_'):
                setting_key = key.replace('setting_', '')
                value = request.POST.get(key)
                
                setting, created = SystemSetting.objects.get_or_create(key=setting_key)
                setting.value = value
                setting.updated_by = request.user
                setting.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('admin_tools:system_settings')
    
    return render(request, 'admin_tools/system_settings.html', {'settings': settings})


@superadmin_required
def audit_logs(request):
    """View audit logs"""
    logs = AuditLog.objects.all()
    
    # Filters
    action_filter = request.GET.get('action', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if action_filter:
        logs = logs.filter(action=action_filter)
    
    if date_from:
        logs = logs.filter(created_at__date__gte=date_from)
    
    if date_to:
        logs = logs.filter(created_at__date__lte=date_to)
    
    paginator = Paginator(logs, 50)
    page = request.GET.get('page')
    logs = paginator.get_page(page)
    
    return render(request, 'admin_tools/audit_logs.html', {
        'logs': logs,
        'action_filter': action_filter
    })


@superadmin_required
def notifications_management(request):
    """Manage notifications"""
    if request.method == 'POST':
        # Send notification to users
        user_ids = request.POST.getlist('users')
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('type', 'info')
        
        if request.POST.get('send_to_all'):
            users = User.objects.filter(is_active=True)
        else:
            users = User.objects.filter(id__in=user_ids)
        
        for user in users:
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type
            )
        
        messages.success(request, f'Notification sent to {users.count()} users.')
        return redirect('admin_tools:notifications_management')
    
    users = User.objects.filter(is_active=True)
    return render(request, 'admin_tools/notifications.html', {'users': users})


@superadmin_required
def reports(request):
    """Generate reports"""
    report_type = request.GET.get('type', 'appointments')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    context = {'report_type': report_type}
    
    if report_type == 'appointments':
        appointments = Appointment.objects.all()
        if date_from:
            appointments = appointments.filter(date__gte=date_from)
        if date_to:
            appointments = appointments.filter(date__lte=date_to)
        
        context['data'] = appointments
        context['stats'] = {
            'total': appointments.count(),
            'completed': appointments.filter(status='completed').count(),
            'cancelled': appointments.filter(status='cancelled').count(),
            'pending': appointments.filter(status='pending').count(),
        }
    
    elif report_type == 'users':
        users = User.objects.all()
        if date_from:
            users = users.filter(created_at__date__gte=date_from)
        if date_to:
            users = users.filter(created_at__date__lte=date_to)
        
        context['data'] = users
        context['stats'] = {
            'total': users.count(),
            'patients': users.filter(role='patient').count(),
            'doctors': users.filter(role='doctor').count(),
            'staff': users.filter(role='staff').count(),
        }
    
    return render(request, 'admin_tools/reports.html', context)


@superadmin_required
def export_data(request):
    """Export data as CSV"""
    import csv
    from io import StringIO
    
    export_type = request.GET.get('type', 'users')
    
    output = StringIO()
    writer = csv.writer(output)
    
    if export_type == 'users':
        writer.writerow(['Email', 'Name', 'Role', 'Phone', 'Created At'])
        for user in User.objects.all():
            writer.writerow([
                user.email,
                user.get_full_name(),
                user.role,
                user.phone,
                user.created_at.strftime('%Y-%m-%d')
            ])
    
    elif export_type == 'appointments':
        writer.writerow(['ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status'])
        for apt in Appointment.objects.all():
            writer.writerow([
                apt.appointment_id,
                apt.patient.get_full_name(),
                apt.doctor.user.get_full_name(),
                apt.date,
                apt.time,
                apt.status
            ])
    
    output.seek(0)
    response = HttpResponse(output.read(), content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{export_type}_export.csv"'
    return response