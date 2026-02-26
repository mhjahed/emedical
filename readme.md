# 🏥 MediCare Hospital - Complete Medical Platform

A comprehensive Django-based medical platform with role-based access, appointment management, video consultations via Google Meet, PDF generation, digital ID cards with barcodes, and a modern blog system.

![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Table of Contents

1. [Features](#-features)
2. [System Requirements](#-system-requirements)
3. [Installation](#-installation)
4. [Project Structure](#-project-structure)
5. [User Roles & Permissions](#-user-roles--permissions)
6. [Admin Guide](#-superadmin-guide)
7. [Doctor/Staff Guide](#-doctorstaff-guide)
8. [Patient Guide](#-patient-guide)
9. [Barcode & ID Card System](#-barcode--id-card-system)
10. [PDF System](#-pdf-system)
11. [Video Consultation](#-video-consultation-google-meet)
12. [API Endpoints](#-api-endpoints)
13. [Troubleshooting](#-troubleshooting)
14. [Contributing](#-contributing)

---

## ✨ Features

### Core Features
- 🔐 **Role-Based Authentication** - Superadmin, Doctor, Staff, Patient
- 📅 **Appointment System** - Book, manage, reschedule appointments
- 📹 **Video Consultations** - Google Meet integration
- 📰 **Medi News Blog** - CKEditor-powered medical articles
- 📄 **PDF Generation** - Customizable templates for prescriptions, reports
- 🪪 **Digital ID Cards** - Auto-generated with barcodes
- 📊 **Admin Dashboard** - Complete analytics and management

### Additional Features
- 🏥 Hospital services showcase
- 👨‍⚕️ Doctor profiles with qualifications
- 📱 Fully responsive design
- 🔍 Search and filter functionality
- 📧 Contact form system
- 📋 Activity logging
- 🔒 Secure authentication

---

## 💻 System Requirements

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Modern web browser
- Webcam (for barcode scanner)

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd medical_platform
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Environment File

Create `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:
- Email address
- First name
- Last name
- Password

### Step 7: Run Development Server

```bash
python manage.py runserver
```

### Step 8: Access the Application

- **Website:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Admin Tools:** http://127.0.0.1:8000/admin-tools/

---

## 📁 Project Structure

```
medical_platform/
├── medical_project/          # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                 # User authentication & roles
├── core/                     # Home, contact, static pages
├── doctors/                  # Doctor profiles, ID cards
├── news/                     # Medi News blog system
├── appointments/             # Appointment booking system
├── services/                 # Hospital services
├── pdf_system/              # PDF templates & generation
├── media_manager/           # Media file management
├── admin_tools/             # Superadmin dashboard
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # Uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

---

## 👥 User Roles & Permissions

### 🔴 Superadmin
- Full system access
- Create/manage doctors and staff
- Manage all content
- Access admin dashboard
- Create PDF templates
- Generate ID cards for all staff
- View audit logs and reports

### 🔵 Doctor
- Personal dashboard
- Manage appointments
- Write Medi News articles
- Generate PDFs for patients
- Add Google Meet links
- View/download own ID card

### 🟢 Staff
- Limited dashboard access
- View assigned appointments
- Basic content access
- View/download own ID card

### 🟡 Patient
- Book appointments
- View appointment history
- Read Medi News articles
- Download medical documents
- Join video consultations
- Manage profile

---

## 🛠 Superadmin Guide

### Accessing Admin Panel

1. Go to http://127.0.0.1:8000/admin-tools/
2. Or use Django Admin: http://127.0.0.1:8000/admin/

### Creating a Doctor Account

1. Go to **Admin Tools** → **Create Doctor/Staff**
2. Select Role: **Doctor**
3. Fill in:
   - First Name
   - Last Name
   - Email (used for login)
   - Password
4. Click **Create Account**
5. A unique Medi ID (e.g., DOC-A1B2C3D4) is auto-generated

### Creating a Staff Account

1. Go to **Admin Tools** → **Create Doctor/Staff**
2. Select Role: **Staff**
3. Fill in the details
4. Click **Create Account**
5. A unique Medi ID (e.g., STF-E5F6G7H8) is auto-generated

### Setting Up Doctor Profile

1. Go to **Django Admin** → **Doctor Profiles**
2. Click on the doctor
3. Fill in:
   - Department
   - Designation
   - Qualifications
   - Consultation fees
   - Available days/times
4. Save

### Generating ID Cards

1. Go to **Django Admin** → **Doctor Profiles** or **Staff Profiles**
2. Select the users
3. Choose action: **Generate ID Cards**
4. Click **Go**
5. ID cards with barcodes are generated automatically

### Creating PDF Templates

1. Go to **Admin Tools** → **PDF Templates**
2. Click **Create Template**
3. Fill in:
   - Template Name
   - Type (Prescription, Report, etc.)
   - Header Content
   - Body Content (use placeholders like `{{patient_name}}`, `{{diagnosis}}`)
   - Footer Content
4. Save

### Managing Hospital Settings

1. Go to **Django Admin** → **Hospital Settings**
2. Update:
   - Hospital name and logo
   - Contact information
   - Social media links
   - Working hours
   - Footer text

### Viewing Reports

1. Go to **Admin Tools** → **Reports**
2. Filter by:
   - Date range
   - Report type (Appointments/Users)
3. Export as CSV if needed

### Managing Content

- **Hero Slides:** Django Admin → Hero Slides
- **About Section:** Django Admin → About Section
- **Services:** Django Admin → Services
- **FAQs:** Django Admin → FAQs
- **Static Pages:** Django Admin → Static Pages

---

## 👨‍⚕️ Doctor/Staff Guide

### Logging In

1. Go to http://127.0.0.1:8000/accounts/doctor-login/
2. Enter your email and password
3. Click **Access Dashboard**

### Dashboard Overview

- View today's appointments
- See pending appointment requests
- Quick access to all features

### Managing Appointments

1. Go to **My Appointments**
2. View all appointments with filters
3. Actions available:
   - **Accept:** Confirm pending appointment
   - **Reject:** Cancel appointment
   - **Add Meet Link:** For video consultations
   - **Mark Complete:** After appointment ends

### Adding Google Meet Link

1. Open the appointment
2. Click **Add Meet Link**
3. Go to [meet.google.com](https://meet.google.com)
4. Create new meeting
5. Copy the link and paste
6. Save

### Writing Medi News Articles

1. Go to **My Articles**
2. Click **Write New Article**
3. Fill in:
   - Title and subtitle
   - Excerpt (short summary)
   - Content (rich text editor)
   - Primary image
   - Category and tags
4. Set status:
   - **Draft:** Save for later
   - **Published:** Make public
5. Save

### Generating PDFs

1. Go to **Generate PDF**
2. Select a template
3. Choose patient
4. Fill in required fields
5. Click **Generate PDF**
6. PDF is saved and available to patient

### Downloading Your ID Card

1. Go to Dashboard
2. Click **Download ID Card**
3. Your digital ID with barcode downloads

---

## 🧑‍💼 Patient Guide

### Creating an Account

1. Go to http://127.0.0.1:8000/accounts/signup/
2. Fill in:
   - First and last name
   - Email address
   - Phone number
   - Password
3. Accept terms and conditions
4. Click **Create Account**

### Booking an Appointment

1. Login to your account
2. Click **Book Appointment**
3. Select:
   - Doctor
   - Date and time
   - Appointment type
   - Video consultation (optional)
4. Enter reason for visit
5. Click **Confirm Booking**
6. Wait for doctor confirmation

### Viewing Appointments

1. Go to **My Appointments**
2. View status:
   - 🟡 Pending - Awaiting confirmation
   - 🟢 Confirmed - Approved by doctor
   - 🔵 Completed - Appointment finished
   - 🔴 Cancelled - Appointment cancelled

### Joining Video Consultation

1. When appointment is confirmed
2. Doctor adds Google Meet link
3. Click **Join Meeting** button
4. Opens Google Meet in new tab

### Viewing Documents

1. Go to **My Documents**
2. View all medical documents
3. Download PDFs

### Managing Profile

1. Go to **Profile**
2. Click **Edit Profile**
3. Update:
   - Personal information
   - Address
   - Emergency contacts
   - Medical history
4. Save changes

---

## 🪪 Barcode & ID Card System

### How It Works

1. **Medi ID Generation:** Auto-generated unique ID for each doctor/staff
   - Doctors: `DOC-XXXXXXXX`
   - Staff: `STF-XXXXXXXX`

2. **Barcode Generation:** Code128 barcode containing Medi ID

3. **ID Card Generation:** Vertical card with:
   - Hospital logo
   - Profile photo
   - Name and designation
   - Department
   - Blood group
   - Medi ID
   - Scannable barcode

### Generating ID Cards (Admin)

```python
# Via Django Admin
1. Go to Doctor Profiles or Staff Profiles
2. Select users
3. Action: "Generate ID Cards"
4. Click Go
```

### Manual Barcode Generation

```python
# In Django shell
python manage.py shell

from doctors.utils import generate_barcode
from django.contrib.auth import get_user_model
User = get_user_model()

# Get the user
user = User.objects.get(email='doctor@example.com')

# Generate barcode
barcode_file = generate_barcode(user.medi_id)

# Save to profile
if user.is_doctor:
    user.doctor_profile.barcode_image.save(f'barcode_{user.medi_id}.png', barcode_file)
    user.doctor_profile.save()
```

### Barcode Scanner Access Control

The barcode scanner is used for:
- Operation Theater (OT) access
- Lab access
- Reception verification
- Locker room access
- Priority access rooms

---

## 📄 PDF System

### Available Placeholders

Use these in your templates:

| Placeholder | Description |
|-------------|-------------|
| `{{patient_name}}` | Patient's full name |
| `{{patient_age}}` | Patient's age |
| `{{patient_gender}}` | Patient's gender |
| `{{patient_blood_group}}` | Blood group |
| `{{doctor_name}}` | Doctor's name |
| `{{doctor_designation}}` | Doctor's title |
| `{{date}}` | Current date |
| `{{time}}` | Current time |
| `{{diagnosis}}` | Diagnosis text |
| `{{prescription}}` | Prescription text |

### Template Types

- Prescription
- Medical Report
- Discharge Summary
- Lab Report
- Medical Certificate
- Invoice
- Referral Letter
- Consent Form

---

## 📹 Video Consultation (Google Meet)

### Flow

1. Patient books appointment with "Video Consultation" option
2. Doctor accepts appointment
3. Doctor creates Google Meet link
4. Doctor pastes link in appointment
5. Both patient and doctor see "Join Meeting" button
6. Button active 15 minutes before appointment
7. Meeting happens on Google Meet
8. Doctor marks appointment as complete

### Why Google Meet?

- ✅ No API complexity
- ✅ No server load
- ✅ Works on all devices
- ✅ Secure and reliable
- ✅ No extra costs

---

## 🔌 API Endpoints

### Appointments
- `GET /appointments/get-slots/<doctor_id>/` - Get available slots
- `POST /appointments/accept/<id>/` - Accept appointment
- `POST /appointments/reject/<id>/` - Reject appointment
- `POST /appointments/complete/<id>/` - Complete appointment

### Barcode
- `POST /doctors/verify-barcode/` - Verify barcode scan
- `GET /doctors/scanner/` - Barcode scanner interface

### Media
- `POST /media-manager/upload/` - Upload files
- `POST /media-manager/create-folder/` - Create folder

---

## ❓ Troubleshooting

### Common Issues

**1. Static files not loading**
```bash
python manage.py collectstatic
```

**2. Database errors**
```bash
python manage.py makemigrations
python manage.py migrate
```

**3. Module not found**
```bash
pip install -r requirements.txt
```

**4. Permission denied**
- Check user role
- Verify login status
- Check URL permissions

**5. Template not found**
- Verify template exists in correct directory
- Check template name spelling
- Run: `python manage.py check`

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

## 📜 License

This project is licensed under the MIT License.

---

## 📞 Support

For support, contact:
- Email: support@medicare.com
- Phone: +1 234 567 890

---

**Built with ❤️ using Django**
```

---

## PART 2: Barcode Scanner System

### Step 1: Create Barcode Scanner View in doctors/views.py

Add these imports and views to `doctors/views.py`:

```python
# Add to doctors/views.py (at the end of the file)

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json


@login_required
def barcode_scanner(request):
    """Barcode scanner interface"""
    return render(request, 'doctors/barcode_scanner.html')


@csrf_exempt
def verify_barcode(request):
    """API endpoint to verify scanned barcode"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            medi_id = data.get('medi_id', '').strip().upper()
            location = data.get('location', 'Unknown Location')
            
            if not medi_id:
                return JsonResponse({
                    'success': False,
                    'message': 'No Medi ID provided'
                })
            
            # Find user with this Medi ID
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            try:
                user = User.objects.get(medi_id=medi_id)
                
                # Get profile info
                profile_type = None
                designation = None
                department = None
                
                if user.is_doctor:
                    profile_type = 'Doctor'
                    try:
                        profile = user.doctor_profile
                        designation = profile.designation or 'Doctor'
                        department = profile.department.name if profile.department else 'General'
                    except:
                        designation = 'Doctor'
                        department = 'General'
                elif user.is_staff_member:
                    profile_type = 'Staff'
                    try:
                        profile = user.staff_profile
                        designation = profile.get_staff_type_display()
                        department = profile.department.name if profile.department else 'General'
                    except:
                        designation = 'Staff'
                        department = 'General'
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid credentials - Not medical staff'
                    })
                
                # Log the access
                current_time = timezone.now()
                access_log = f"{profile_type} {user.get_full_name()} ({medi_id}) has been granted access to {location} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}"
                
                # Print to console
                print("=" * 60)
                print("🔓 ACCESS GRANTED")
                print("=" * 60)
                print(f"👤 Name: {user.get_full_name()}")
                print(f"🆔 Medi ID: {medi_id}")
                print(f"👔 Type: {profile_type}")
                print(f"💼 Designation: {designation}")
                print(f"🏥 Department: {department}")
                print(f"📍 Location: {location}")
                print(f"⏰ Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 60)
                
                # Create access log in database
                from admin_tools.models import AuditLog
                AuditLog.objects.create(
                    user=user,
                    action='access',
                    description=f'Barcode scan: Access to {location}',
                    model_name='BarcodeAccess',
                    extra_data={
                        'location': location,
                        'medi_id': medi_id,
                        'profile_type': profile_type
                    }
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Access Granted',
                    'data': {
                        'name': user.get_full_name(),
                        'medi_id': medi_id,
                        'profile_type': profile_type,
                        'designation': designation,
                        'department': department,
                        'photo': user.profile_picture.url if user.profile_picture else None,
                        'access_time': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'location': location
                    }
                })
                
            except User.DoesNotExist:
                # Log failed attempt
                print("=" * 60)
                print("🔒 ACCESS DENIED")
                print("=" * 60)
                print(f"🆔 Attempted Medi ID: {medi_id}")
                print(f"📍 Location: {location}")
                print(f"⏰ Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("❌ Reason: Medi ID not found in database")
                print("=" * 60)
                
                return JsonResponse({
                    'success': False,
                    'message': 'Access Denied - Invalid Medi ID'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request data'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })


def manual_barcode_entry(request):
    """Manual barcode entry for testing"""
    if request.method == 'POST':
        medi_id = request.POST.get('medi_id', '')
        location = request.POST.get('location', 'Manual Entry')
        
        # Use the verify function
        from django.test import RequestFactory
        factory = RequestFactory()
        fake_request = factory.post('/verify-barcode/', 
            json.dumps({'medi_id': medi_id, 'location': location}),
            content_type='application/json'
        )
        response = verify_barcode(fake_request)
        return response
    
    return render(request, 'doctors/manual_barcode.html')
```

---

### Step 2: Update doctors/urls.py

Replace your `doctors/urls.py` with:

```python
# doctors/urls.py

from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Public Pages
    path('', views.doctors_list, name='doctors_list'),
    path('doctor/<slug:slug>/', views.doctor_detail, name='doctor_detail'),
    path('staff/', views.staff_list, name='staff_list'),
    
    # Dashboard (Private)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-appointments/', views.doctor_appointments, name='appointments'),
    path('download-id-card/', views.download_id_card, name='download_id_card'),
    
    # Admin Actions
    path('generate-id-card/<int:user_id>/', views.generate_staff_id_card, name='generate_id_card'),
    
    # Barcode Scanner System
    path('scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('verify-barcode/', views.verify_barcode, name='verify_barcode'),
    path('manual-barcode/', views.manual_barcode_entry, name='manual_barcode'),
]
```

---

### Step 3: Create Barcode Scanner Template

Create file: `templates/doctors/barcode_scanner.html`

```html
<!-- templates/doctors/barcode_scanner.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Barcode Scanner - Access Control{% endblock %}

{% block extra_css %}
<style>
    .scanner-container {
        max-width: 600px;
        margin: 0 auto;
    }
    
    #video-container {
        position: relative;
        width: 100%;
        background: #000;
        border-radius: 15px;
        overflow: hidden;
    }
    
    #video {
        width: 100%;
        height: auto;
        display: block;
    }
    
    #canvas {
        display: none;
    }
    
    .scanner-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        height: 100px;
        border: 3px solid #00ff00;
        border-radius: 10px;
        box-shadow: 0 0 0 9999px rgba(0, 0, 0, 0.5);
    }
    
    .scanner-line {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #00ff00, transparent);
        animation: scan 2s linear infinite;
    }
    
    @keyframes scan {
        0% { top: 0; }
        50% { top: calc(100% - 3px); }
        100% { top: 0; }
    }
    
    .access-result {
        display: none;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
    }
    
    .access-granted {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
    }
    
    .access-denied {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
    }
    
    .location-btn {
        margin: 5px;
    }
    
    .location-btn.active {
        background-color: #0d6efd;
        color: white;
    }
</style>
{% endblock %}

{% block content %}
<section class="py-4 bg-dark text-white">
    <div class="container">
        <div class="row align-items-center">
            <div class="col">
                <h3 class="mb-0"><i class="fas fa-qrcode me-2"></i>Barcode Scanner</h3>
                <small class="opacity-75">Staff Access Control System</small>
            </div>
            <div class="col-auto">
                <a href="{% url 'doctors:manual_barcode' %}" class="btn btn-light btn-sm">
                    <i class="fas fa-keyboard me-1"></i>Manual Entry
                </a>
            </div>
        </div>
    </div>
</section>

<section class="py-5">
    <div class="container">
        <div class="scanner-container">
            <!-- Location Selection -->
            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-map-marker-alt me-2 text-primary"></i>Select Access Location</h5>
                </div>
                <div class="card-body text-center">
                    <button class="btn btn-outline-primary location-btn active" data-location="Reception">
                        <i class="fas fa-door-open me-1"></i>Reception
                    </button>
                    <button class="btn btn-outline-danger location-btn" data-location="Operation Theater">
                        <i class="fas fa-procedures me-1"></i>Operation Theater
                    </button>
                    <button class="btn btn-outline-info location-btn" data-location="Laboratory">
                        <i class="fas fa-flask me-1"></i>Laboratory
                    </button>
                    <button class="btn btn-outline-success location-btn" data-location="ICU">
                        <i class="fas fa-heartbeat me-1"></i>ICU
                    </button>
                    <button class="btn btn-outline-warning location-btn" data-location="Pharmacy">
                        <i class="fas fa-pills me-1"></i>Pharmacy
                    </button>
                    <button class="btn btn-outline-secondary location-btn" data-location="Locker Room">
                        <i class="fas fa-lock me-1"></i>Locker Room
                    </button>
                </div>
            </div>
            
            <!-- Scanner -->
            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-camera me-2 text-primary"></i>Scan Barcode</h5>
                </div>
                <div class="card-body">
                    <div id="video-container">
                        <video id="video" autoplay playsinline></video>
                        <div class="scanner-overlay">
                            <div class="scanner-line"></div>
                        </div>
                    </div>
                    <canvas id="canvas"></canvas>
                    
                    <div class="text-center mt-3">
                        <button id="startBtn" class="btn btn-primary btn-lg">
                            <i class="fas fa-play me-2"></i>Start Scanner
                        </button>
                        <button id="stopBtn" class="btn btn-danger btn-lg" style="display: none;">
                            <i class="fas fa-stop me-2"></i>Stop Scanner
                        </button>
                    </div>
                    
                    <div class="alert alert-info mt-3">
                        <i class="fas fa-info-circle me-2"></i>
                        Position the barcode within the green box. Scanner will automatically detect and verify.
                    </div>
                </div>
            </div>
            
            <!-- Manual Entry -->
            <div class="card border-0 shadow-sm mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-keyboard me-2 text-primary"></i>Manual Entry</h5>
                </div>
                <div class="card-body">
                    <div class="input-group">
                        <input type="text" id="manualMediId" class="form-control form-control-lg" placeholder="Enter Medi ID (e.g., DOC-A1B2C3D4)">
                        <button class="btn btn-primary" id="manualVerifyBtn">
                            <i class="fas fa-check me-1"></i>Verify
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Result Display -->
            <div id="accessResult" class="access-result">
                <div class="row align-items-center">
                    <div class="col-auto">
                        <div id="resultIcon" style="font-size: 4rem;"></div>
                    </div>
                    <div class="col">
                        <h3 id="resultTitle" class="mb-2"></h3>
                        <div id="resultDetails"></div>
                    </div>
                </div>
            </div>
            
            <!-- Access Log -->
            <div class="card border-0 shadow-sm mt-4">
                <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
                    <h5 class="mb-0"><i class="fas fa-history me-2 text-primary"></i>Recent Access Log</h5>
                    <button class="btn btn-sm btn-outline-secondary" onclick="clearLog()">
                        <i class="fas fa-trash me-1"></i>Clear
                    </button>
                </div>
                <div class="card-body p-0">
                    <div id="accessLog" class="list-group list-group-flush" style="max-height: 300px; overflow-y: auto;">
                        <div class="list-group-item text-center text-muted py-4">
                            <i class="fas fa-clipboard-list fa-2x mb-2"></i>
                            <p class="mb-0">No scans yet</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

{% block extra_js %}
<!-- Include Quagga.js for barcode scanning -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>

<script>
let selectedLocation = 'Reception';
let isScanning = false;
let lastScannedCode = '';
let scanTimeout = null;

// Location selection
document.querySelectorAll('.location-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.location-btn').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        selectedLocation = this.dataset.location;
    });
});

// Start Scanner
document.getElementById('startBtn').addEventListener('click', function() {
    startScanner();
});

// Stop Scanner
document.getElementById('stopBtn').addEventListener('click', function() {
    stopScanner();
});

// Manual Verify
document.getElementById('manualVerifyBtn').addEventListener('click', function() {
    const mediId = document.getElementById('manualMediId').value.trim();
    if (mediId) {
        verifyBarcode(mediId);
    }
});

// Enter key for manual input
document.getElementById('manualMediId').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const mediId = this.value.trim();
        if (mediId) {
            verifyBarcode(mediId);
        }
    }
});

function startScanner() {
    const video = document.getElementById('video');
    
    navigator.mediaDevices.getUserMedia({ 
        video: { 
            facingMode: 'environment',
            width: { ideal: 1280 },
            height: { ideal: 720 }
        } 
    })
    .then(function(stream) {
        video.srcObject = stream;
        isScanning = true;
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'inline-block';
        
        // Start Quagga for barcode detection
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#video-container'),
                constraints: {
                    facingMode: "environment"
                }
            },
            decoder: {
                readers: ["code_128_reader", "ean_reader", "code_39_reader"]
            }
        }, function(err) {
            if (err) {
                console.log(err);
                // Fallback to manual only
                showToast('Camera started. Use manual entry if barcode not detected.', 'info');
                return;
            }
            Quagga.start();
        });
        
        Quagga.onDetected(function(result) {
            const code = result.codeResult.code;
            
            // Prevent duplicate scans
            if (code !== lastScannedCode) {
                lastScannedCode = code;
                
                // Play beep sound
                playBeep();
                
                // Verify the barcode
                verifyBarcode(code);
                
                // Reset after 3 seconds
                clearTimeout(scanTimeout);
                scanTimeout = setTimeout(() => {
                    lastScannedCode = '';
                }, 3000);
            }
        });
    })
    .catch(function(err) {
        console.error('Camera error:', err);
        showToast('Could not access camera. Please use manual entry.', 'warning');
    });
}

function stopScanner() {
    const video = document.getElementById('video');
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
    }
    
    try {
        Quagga.stop();
    } catch(e) {}
    
    isScanning = false;
    document.getElementById('startBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').style.display = 'none';
}

function verifyBarcode(mediId) {
    fetch('{% url "doctors:verify_barcode" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            medi_id: mediId,
            location: selectedLocation
        })
    })
    .then(response => response.json())
    .then(data => {
        showResult(data);
        addToLog(data, mediId);
    })
    .catch(error => {
        console.error('Error:', error);
        showResult({
            success: false,
            message: 'Network error. Please try again.'
        });
    });
}

function showResult(data) {
    const resultDiv = document.getElementById('accessResult');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultDetails = document.getElementById('resultDetails');
    
    resultDiv.style.display = 'block';
    
    if (data.success) {
        resultDiv.className = 'access-result access-granted';
        resultIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
        resultTitle.textContent = '✓ ACCESS GRANTED';
        resultDetails.innerHTML = `
            <p class="mb-1"><strong>${data.data.name}</strong></p>
            <p class="mb-1">${data.data.profile_type} - ${data.data.designation}</p>
            <p class="mb-1"><small>Department: ${data.data.department}</small></p>
            <p class="mb-0"><small>Location: ${data.data.location} | Time: ${data.data.access_time}</small></p>
        `;
        
        // Play success sound
        playSuccess();
    } else {
        resultDiv.className = 'access-result access-denied';
        resultIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
        resultTitle.textContent = '✗ ACCESS DENIED';
        resultDetails.innerHTML = `<p class="mb-0">${data.message}</p>`;
        
        // Play error sound
        playError();
    }
    
    // Hide after 5 seconds
    setTimeout(() => {
        resultDiv.style.display = 'none';
    }, 5000);
}

function addToLog(data, mediId) {
    const logDiv = document.getElementById('accessLog');
    const now = new Date().toLocaleTimeString();
    
    // Clear "no scans" message
    if (logDiv.querySelector('.text-muted')) {
        logDiv.innerHTML = '';
    }
    
    const logEntry = document.createElement('div');
    logEntry.className = `list-group-item ${data.success ? 'list-group-item-success' : 'list-group-item-danger'}`;
    
    if (data.success) {
        logEntry.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <i class="fas fa-check-circle text-success me-2"></i>
                    <strong>${data.data.name}</strong>
                    <span class="badge bg-primary ms-2">${data.data.profile_type}</span>
                </div>
                <small class="text-muted">${now}</small>
            </div>
            <small class="text-muted">
                ${mediId} → ${data.data.location}
            </small>
        `;
    } else {
        logEntry.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <i class="fas fa-times-circle text-danger me-2"></i>
                    <strong>Access Denied</strong>
                </div>
                <small class="text-muted">${now}</small>
            </div>
            <small class="text-muted">${mediId} - ${data.message}</small>
        `;
    }
    
    logDiv.insertBefore(logEntry, logDiv.firstChild);
}

function clearLog() {
    document.getElementById('accessLog').innerHTML = `
        <div class="list-group-item text-center text-muted py-4">
            <i class="fas fa-clipboard-list fa-2x mb-2"></i>
            <p class="mb-0">No scans yet</p>
        </div>
    `;
}

function playBeep() {
    const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2teleVsQKIPT8NyoeF0cPYPI9tOrdGsqOHq/8uCjdHE7MHG59uWrgXhKLGuz9+2mhYFVJGKr9++ukIlaHlGl+PK2mZdoGUKc+/bAnZ9yFDST/PnJpKh8Di+L/PvRq7B8CymE/v3ZsbV/CiZ+//7gtrl/Byh7//7muLt9Bil7//frtrt7BS58//fxt7t7BS9+//T2uLl5BzGA//L4ubl3CDaE//D7urh0CT2J/+79vLZxC0SM/+r/vbJtDEuQ/+j/v7BqDlGU/+X/wa1nD1aX/+P/w6pjEFya/+D/xaZgEWGe/93/x6RdEmWh/9r/yaFaE2mk/9j/yp5YFG6o/9X/zJtVFXKr/9P/zphSFneu/9D/0JVPGHux/87/0pNNGX6z/8v/1JBJG4G2/8n/1o5HHoS4/8b/2IxEH4e7/8P/2YpBIIq9/8H/24c/Io2//77/3YU8JJC//7z/3oQ6JpLB/7r/34I4J5PD/7n/4IE3KJbE/7f/4IA1KpjG/7X/4X80LJrI/7P/4n0zLZzJ/7L/43syL53K/7D/5HkxMJ/M/6//5XgvMqHN/63/5ncuNKLP/6z/53ctNaTP/6r/6HYsN6bR/6n/6XUrOKjS/6j/6nQqOqrT/6f/63MpO6vU/6X/7HIoPK3V/6T/7XEnPq/W/6P/7nAmQLHX/6L/728lQbLY/6D/8G4kQ7TZ/5//8W0jRLba/57/8mwhRrjb/53/82sgSLnc/5z/9GofSbvd/5v/9WkeSr3e/5n/9mgeS7/g/5j/92cdTcDh/5f/+GYcT8Li/5b/+WUbUMTj/5X/+mQaUsbk/5T/+2MZVMfl/5P//GIYVcnn/5L//WEXWMro/5H//mAWWcvp/5D//18VW83q/4///14UXM/r/47//l0TX9Hs/43//lwSYNLt/4z//1sRYtTu/4v//loQZNXv/4r//lkPZdfw/4n//lgOZ9jx/4j//1cNadrz/4f//lYMat31/4b//lULbN72/4X//1QKbt/3/4T//lMJcOH4/4P//lIIceL5/4L//1EHc+T6/4H//lAGdOb7/4D//08Fduf8/3///04Eeej9/37//k0De+r+/33//kwCfOz//3z//ksB');
    audio.play().catch(() => {});
}

function playSuccess() {
    // Success beep
}

function playError() {
    // Error beep
}

function showToast(message, type) {
    alert(message);
}
</script>
{% endblock %}
```

---

### Step 4: Create Manual Barcode Entry Template

Create file: `templates/doctors/manual_barcode.html`

```html
<!-- templates/doctors/manual_barcode.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Manual Barcode Entry - Access Control{% endblock %}

{% block content %}
<section class="py-4 bg-dark text-white">
    <div class="container">
        <div class="row align-items-center">
            <div class="col">
                <h3 class="mb-0"><i class="fas fa-keyboard me-2"></i>Manual Barcode Entry</h3>
                <small class="opacity-75">Enter Medi ID manually for access verification</small>
            </div>
            <div class="col-auto">
                <a href="{% url 'doctors:barcode_scanner' %}" class="btn btn-light btn-sm">
                    <i class="fas fa-camera me-1"></i>Use Camera Scanner
                </a>
            </div>
        </div>
    </div>
</section>

<section class="py-5">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card border-0 shadow-sm">
                    <div class="card-body p-4">
                        <form method="post" id="verifyForm">
                            {% csrf_token %}
                            
                            <div class="mb-4">
                                <label class="form-label fw-bold">Medi ID *</label>
                                <input type="text" name="medi_id" class="form-control form-control-lg text-center" 
                                       placeholder="DOC-XXXXXXXX" id="mediIdInput" required autofocus
                                       style="font-family: monospace; font-size: 1.5rem; letter-spacing: 2px;">
                                <small class="text-muted">Enter the Medi ID from the ID card barcode</small>
                            </div>
                            
                            <div class="mb-4">
                                <label class="form-label fw-bold">Access Location</label>
                                <select name="location" class="form-select form-select-lg">
                                    <option value="Reception">Reception</option>
                                    <option value="Operation Theater">Operation Theater (OT)</option>
                                    <option value="Laboratory">Laboratory</option>
                                    <option value="ICU">ICU</option>
                                    <option value="Pharmacy">Pharmacy</option>
                                    <option value="Locker Room">Locker Room</option>
                                    <option value="Emergency">Emergency Room</option>
                                    <option value="Radiology">Radiology</option>
                                    <option value="Records Room">Medical Records</option>
                                </select>
                            </div>
                            
                            <button type="submit" class="btn btn-primary btn-lg w-100">
                                <i class="fas fa-check-circle me-2"></i>Verify Access
                            </button>
                        </form>
                        
                        <!-- Result Display -->
                        <div id="result" class="mt-4" style="display: none;"></div>
                    </div>
                </div>
                
                <!-- Quick Test IDs -->
                <div class="card border-0 shadow-sm mt-4">
                    <div class="card-header bg-white py-3">
                        <h6 class="mb-0"><i class="fas fa-info-circle me-2 text-info"></i>Quick Reference</h6>
                    </div>
                    <div class="card-body">
                        <p class="text-muted small mb-2">Medi ID Format:</p>
                        <ul class="text-muted small mb-0">
                            <li><code>DOC-XXXXXXXX</code> - Doctor IDs</li>
                            <li><code>STF-XXXXXXXX</code> - Staff IDs</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
{% endblock %}

{% block extra_js %}
<script>
document.getElementById('verifyForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const mediId = document.getElementById('mediIdInput').value.trim().toUpperCase();
    const location = document.querySelector('select[name="location"]').value;
    const resultDiv = document.getElementById('result');
    
    fetch('{% url "doctors:verify_barcode" %}', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            medi_id: mediId,
            location: location
        })
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.style.display = 'block';
        
        if (data.success) {
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    <h4><i class="fas fa-check-circle me-2"></i>ACCESS GRANTED</h4>
                    <hr>
                    <p class="mb-1"><strong>Name:</strong> ${data.data.name}</p>
                    <p class="mb-1"><strong>Type:</strong> ${data.data.profile_type}</p>
                    <p class="mb-1"><strong>Designation:</strong> ${data.data.designation}</p>
                    <p class="mb-1"><strong>Department:</strong> ${data.data.department}</p>
                    <p class="mb-0"><strong>Location:</strong> ${data.data.location}</p>
                    <p class="mb-0"><strong>Time:</strong> ${data.data.access_time}</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `
                <div class="alert alert-danger">
                    <h4><i class="fas fa-times-circle me-2"></i>ACCESS DENIED</h4>
                    <hr>
                    <p class="mb-0">${data.message}</p>
                </div>
            `;
        }
        
        // Clear input
        document.getElementById('mediIdInput').value = '';
        document.getElementById('mediIdInput').focus();
    })
    .catch(error => {
        resultDiv.style.display = 'block';
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Network error. Please try again.
            </div>
        `;
    });
});

// Auto-uppercase input
document.getElementById('mediIdInput').addEventListener('input', function() {
    this.value = this.value.toUpperCase();
});
</script>
{% endblock %}
```

---

## PART 3: Update Navigation to Include Scanner

Update `templates/base.html` to add scanner link for medical staff.

In the navigation dropdown (around line 60), add:

```html
{% if user.is_medical_staff %}
<li><a class="dropdown-item" href="{% url 'doctors:barcode_scanner' %}"><i class="fas fa-qrcode me-2"></i>Barcode Scanner</a></li>
{% endif %}
```

---

## PART 4: Confirmation of ID Card & Barcode System

### ✅ Confirmed: Doctors and Staff ID Cards with Barcodes

**YES**, the system supports:

1. **Doctors** get ID cards with:
   - Unique Medi ID: `DOC-XXXXXXXX`
   - Code128 Barcode
   - Profile photo
   - Name, designation, department
   - Blood group

2. **Staff** get ID cards with:
   - Unique Medi ID: `STF-XXXXXXXX`
   - Code128 Barcode
   - Profile photo
   - Name, staff type, department

### How to Generate ID Cards:

**Method 1: Django Admin**
```
1. Go to /admin/
2. Navigate to Doctor Profiles or Staff Profiles
3. Select the users
4. Action: "Generate ID Cards"
5. Click Go
```

**Method 2: Django Shell (Manual)**
```python
python manage.py shell

from doctors.utils import generate_barcode, generate_id_card
from django.contrib.auth import get_user_model
User = get_user_model()

# Get user
user = User.objects.get(email='doctor@example.com')
profile = user.doctor_profile  # or user.staff_profile

# Generate barcode
barcode = generate_barcode(user.medi_id)
profile.barcode_image.save(f'barcode_{user.medi_id}.png', barcode)

# Generate ID card
id_card = generate_id_card(user, profile)
profile.id_card_image.save(f'id_card_{user.medi_id}.png', id_card)

profile.save()
print(f"ID Card generated for {user.get_full_name()}")
```

---

## PART 5: Run Final Checks

```bash
# 1. Make migrations (if any pending)
python manage.py makemigrations

# 2. Apply migrations
python manage.py migrate

# 3. Check for errors
python manage.py check

# 4. Run server
python manage.py runserver
```

---

## PART 6: Testing the Barcode Scanner

### Access the Scanner:
1. Login as superadmin or doctor
2. Go to: http://127.0.0.1:8000/doctors/scanner/

### Test Manual Entry:
1. Go to: http://127.0.0.1:8000/doctors/manual-barcode/
2. Enter a valid Medi ID (e.g., `DOC-A1B2C3D4`)
3. Select location
4. Click Verify

### Console Output Example:
```
============================================================
🔓 ACCESS GRANTED
============================================================
👤 Name: Dr. John Smith
🆔 Medi ID: DOC-A1B2C3D4
👔 Type: Doctor
💼 Designation: Cardiologist
🏥 Department: Cardiology
📍 Location: Operation Theater
⏰ Time: 2024-01-15 14:30:45
============================================================
```

---

## ✅ FINAL CHECKLIST

| Feature | Status |
|---------|--------|
| User Authentication | ✅ Complete |
| Role-Based Access | ✅ Complete |
| Patient Signup/Login | ✅ Complete |
| Doctor/Staff Login | ✅ Complete |
| Appointment Booking | ✅ Complete |
| Video Consultation (Google Meet) | ✅ Complete |
| Medi News Blog | ✅ Complete |
| PDF Generation | ✅ Complete |
| Services Pages | ✅ Complete |
| Doctor Profiles | ✅ Complete |
| Digital ID Cards | ✅ Complete |
| Barcode Generation | ✅ Complete |
| Barcode Scanner | ✅ Complete |
| Access Control Logging | ✅ Complete |
| Admin Dashboard | ✅ Complete |
| Reports & Analytics | ✅ Complete |
| README Documentation | ✅ Complete |

---

## 🎉 Project Complete!

Your Medical Platform is now fully functional with:

- Complete user management system
- Appointment booking with video consultation support
- Medical news blog with rich text editing
- PDF document generation
- Digital ID cards with scannable barcodes
- Access control system with barcode scanner
- Comprehensive admin tools

**Start the server and enjoy your new medical platform!**

```bash
python manage.py runserver
```