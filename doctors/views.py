# doctors/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Department, DoctorProfile, StaffProfile, Specialization
from .utils import generate_id_card, generate_barcode
from accounts.decorators import medical_staff_required, superadmin_required


def doctors_list(request):
    """Public page - List all doctors"""
    doctors = DoctorProfile.objects.filter(is_active=True).select_related('user', 'department')
    departments = Department.objects.filter(is_active=True)
    
    # Search & Filter
    search = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    
    if search:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__medi_id__icontains=search) |
            Q(designation__icontains=search)
        )
    
    if department_filter:
        doctors = doctors.filter(department__slug=department_filter)
    
    paginator = Paginator(doctors, 12)
    page = request.GET.get('page')
    doctors = paginator.get_page(page)
    
    context = {
        'doctors': doctors,
        'departments': departments,
        'search': search,
        'department_filter': department_filter,
    }
    return render(request, 'doctors/doctors_list.html', context)


def doctor_detail(request, slug):
    """Public page - Doctor profile"""
    doctor = get_object_or_404(DoctorProfile, slug=slug, is_active=True)
    
    context = {
        'doctor': doctor,
        'education': doctor.education.all(),
        'experiences': doctor.experiences.all(),
        'awards': doctor.awards.all(),
    }
    return render(request, 'doctors/doctor_detail.html', context)


def staff_list(request):
    """Public page - List all staff"""
    staff = StaffProfile.objects.filter(is_active=True).select_related('user', 'department')
    
    paginator = Paginator(staff, 12)
    page = request.GET.get('page')
    staff = paginator.get_page(page)
    
    return render(request, 'doctors/staff_list.html', {'staff': staff})


@medical_staff_required
def dashboard(request):
    """Doctor/Staff Dashboard"""
    user = request.user
    context = {
        'user': user,
    }
    
    if user.is_doctor:
        try:
            profile = user.doctor_profile
            context['profile'] = profile
            # Get today's appointments
            from appointments.models import Appointment
            from django.utils import timezone
            today = timezone.now().date()
            context['today_appointments'] = Appointment.objects.filter(
                doctor=profile,
                date=today
            ).order_by('time')
            context['pending_appointments'] = Appointment.objects.filter(
                doctor=profile,
                status='pending'
            ).count()
        except DoctorProfile.DoesNotExist:
            pass
    
    return render(request, 'doctors/dashboard.html', context)


@medical_staff_required
def doctor_appointments(request):
    """View doctor's appointments"""
    from appointments.models import Appointment
    
    user = request.user
    appointments = []
    
    if user.is_doctor:
        try:
            profile = user.doctor_profile
            appointments = Appointment.objects.filter(doctor=profile).order_by('-date', '-time')
        except DoctorProfile.DoesNotExist:
            pass
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    paginator = Paginator(appointments, 20)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    
    return render(request, 'doctors/appointments.html', {
        'appointments': appointments,
        'status_filter': status_filter
    })


@medical_staff_required
def download_id_card(request):
    """Download current user's ID card"""
    user = request.user
    profile = None
    
    if user.is_doctor:
        profile = getattr(user, 'doctor_profile', None)
    elif user.is_staff_member:
        profile = getattr(user, 'staff_profile', None)
    
    if not profile:
        messages.error(request, 'Profile not found.')
        return redirect('doctors:dashboard')
    
    # Check if ID card already exists
    if profile.id_card_image:
        response = HttpResponse(profile.id_card_image.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="id_card_{user.medi_id}.png"'
        return response
    
    # Generate new ID card
    id_card = generate_id_card(user, profile)
    if id_card:
        profile.id_card_image.save(f'id_card_{user.medi_id}.png', id_card)
        profile.save()
        
        response = HttpResponse(profile.id_card_image.read(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="id_card_{user.medi_id}.png"'
        return response
    
    messages.error(request, 'Failed to generate ID card.')
    return redirect('doctors:dashboard')


@superadmin_required
def generate_staff_id_card(request, user_id):
    """Admin: Generate ID card for a doctor/staff"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    user = get_object_or_404(User, id=user_id)
    profile = None
    
    if user.is_doctor:
        profile = getattr(user, 'doctor_profile', None)
    elif user.is_staff_member:
        profile = getattr(user, 'staff_profile', None)
    
    if not profile:
        return JsonResponse({'success': False, 'message': 'Profile not found'})
    
    # Generate barcode
    barcode_content = generate_barcode(user.medi_id)
    if barcode_content:
        profile.barcode_image.save(f'barcode_{user.medi_id}.png', barcode_content)
    
    # Generate ID card
    id_card = generate_id_card(user, profile)
    if id_card:
        profile.id_card_image.save(f'id_card_{user.medi_id}.png', id_card)
        profile.save()
        return JsonResponse({
            'success': True, 
            'message': 'ID card generated successfully',
            'id_card_url': profile.id_card_image.url if profile.id_card_image else None
        })
    
    return JsonResponse({'success': False, 'message': 'Failed to generate ID card'})



# -------------------------------
# Manual Barcode Reader (Fallback)
# -------------------------------

from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
@require_http_methods(["GET", "POST"])
def manual_barcode_entry(request):
    """
    Manual barcode entry (keyboard / barcode gun fallback)
    """

    if request.method == "POST":
        medi_id = request.POST.get("medi_id", "").strip().upper()
        location = request.POST.get("location", "Manual Entry")

        if not medi_id:
            return JsonResponse({
                "success": False,
                "message": "Medi ID is required"
            })

        try:
            user = User.objects.get(medi_id=medi_id)

            # Determine role & profile
            if user.is_doctor:
                profile_type = "Doctor"
                profile = user.doctor_profile
                designation = profile.designation
                department = profile.department.name if profile.department else "General"

            elif user.is_staff_member:
                profile_type = "Staff"
                profile = user.staff_profile
                designation = profile.get_staff_type_display()
                department = profile.department.name if profile.department else "General"

            else:
                return JsonResponse({
                    "success": False,
                    "message": "Not authorized medical staff"
                })

            current_time = timezone.now()

            # Console-style log (matches your ACCESS GRANTED output)
            print("=" * 60)
            print("🔓 ACCESS GRANTED (MANUAL)")
            print("=" * 60)
            print(f"👤 Name: {user.get_full_name()}")
            print(f"🆔 Medi ID: {medi_id}")
            print(f"👔 Type: {profile_type}")
            print(f"💼 Designation: {designation}")
            print(f"🏥 Department: {department}")
            print(f"📍 Location: {location}")
            print(f"⏰ Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)

            return JsonResponse({
                "success": True,
                "message": "Access Granted",
                "data": {
                    "name": user.get_full_name(),
                    "medi_id": medi_id,
                    "profile_type": profile_type,
                    "designation": designation,
                    "department": department,
                    "location": location,
                    "access_time": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                }
            })

        except User.DoesNotExist:
            print("=" * 60)
            print("🔒 ACCESS DENIED (MANUAL)")
            print("=" * 60)
            print(f"🆔 Attempted Medi ID: {medi_id}")
            print(f"📍 Location: {location}")
            print(f"⏰ Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("❌ Reason: Medi ID not found")
            print("=" * 60)

            return JsonResponse({
                "success": False,
                "message": "Invalid Medi ID"
            })

    # GET request → show manual entry page
    return render(request, "doctors/manual_barcode.html")

@login_required
def barcode_scanner(request):
    """
    Camera-based barcode scanner page
    """
    return render(request, "doctors/barcode_scanner.html")




import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@require_POST
def verify_barcode(request):
    try:
        data = json.loads(request.body)
        medi_id = data.get("medi_id", "").strip().upper()
        location = data.get("location", "Unknown")

        if not medi_id:
            return JsonResponse({
                "success": False,
                "message": "Invalid Medi ID"
            }, status=400)

        try:
            user = User.objects.get(medi_id=medi_id)
        except User.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Medi ID not found"
            })

        # Determine profile
        if getattr(user, "is_doctor", False):
            profile = user.doctor_profile
            profile_type = "Doctor"
        elif getattr(user, "is_staff_member", False):
            profile = user.staff_profile
            profile_type = "Staff"
        else:
            return JsonResponse({
                "success": False,
                "message": "Unauthorized profile"
            })

        # ✅ SUCCESS RESPONSE (matches your JS exactly)
        return JsonResponse({
            "success": True,
            "data": {
                "name": user.get_full_name(),
                "profile_type": profile_type,
                "designation": getattr(profile, "designation", "N/A"),
                "department": getattr(profile, "department", "N/A"),
                "location": location,
                "access_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "Server error"
        }, status=500)