# core/management/commands/setup_initial_data.py

from django.core.management.base import BaseCommand
from core.models import HospitalSettings, HeroSlide, AboutSection, Feature, FAQ
from appointments.models import TimeSlot
from services.models import ServiceCategory
from doctors.models import Department
from news.models import Category as NewsCategory
from datetime import time


class Command(BaseCommand):
    help = 'Set up initial data for the medical platform'

    def handle(self, *args, **options):
        # Hospital Settings
        hospital, created = HospitalSettings.objects.get_or_create(pk=1)
        if created:
            hospital.name = "MediCare Hospital"
            hospital.tagline = "Your Health, Our Priority"
            hospital.email = "info@medicare.com"
            hospital.phone = "+1 234 567 890"
            hospital.address = "123 Medical Center Boulevard"
            hospital.city = "New York"
            hospital.state = "NY"
            hospital.zip_code = "10001"
            hospital.working_hours = "Mon-Fri: 8:00 AM - 8:00 PM\nSat-Sun: 9:00 AM - 5:00 PM"
            hospital.save()
            self.stdout.write(self.style.SUCCESS('Created hospital settings'))

        # About Section
        about, created = AboutSection.objects.get_or_create(pk=1)
        if created:
            about.title = "About MediCare Hospital"
            about.subtitle = "Committed to Excellence in Healthcare"
            about.content = """
            <p>MediCare Hospital has been providing exceptional healthcare services for over 25 years. 
            Our team of dedicated medical professionals is committed to delivering personalized care 
            with compassion and expertise.</p>
            <p>We combine cutting-edge medical technology with a patient-centered approach to ensure 
            the best possible outcomes for our patients.</p>
            """
            about.years_experience = 25
            about.total_doctors = 50
            about.happy_patients = 10000
            about.total_departments = 15
            about.save()
            self.stdout.write(self.style.SUCCESS('Created about section'))

        # Features
        features_data = [
            {'title': '24/7 Emergency', 'description': 'Round-the-clock emergency services', 'icon': 'fa-ambulance'},
            {'title': 'Expert Doctors', 'description': 'Board-certified specialists', 'icon': 'fa-user-md'},
            {'title': 'Modern Equipment', 'description': 'State-of-the-art medical technology', 'icon': 'fa-microscope'},
            {'title': 'Affordable Care', 'description': 'Quality healthcare at reasonable costs', 'icon': 'fa-hand-holding-usd'},
        ]
        for i, data in enumerate(features_data):
            Feature.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'icon': data['icon'],
                    'order': i
                }
            )
        self.stdout.write(self.style.SUCCESS('Created features'))

        # Departments
        departments_data = [
            'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 
            'Gynecology', 'Dermatology', 'Ophthalmology', 'ENT',
            'General Medicine', 'Surgery'
        ]
        for dept_name in departments_data:
            Department.objects.get_or_create(
                name=dept_name,
                defaults={'slug': dept_name.lower(), 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS('Created departments'))

        # Service Categories
        service_categories = ['Emergency Services', 'Diagnostic Services', 'Surgical Services', 'Preventive Care']
        for cat_name in service_categories:
            ServiceCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': cat_name.lower().replace(' ', '-')}
            )
        self.stdout.write(self.style.SUCCESS('Created service categories'))

        # News Categories
        news_categories = ['Health Tips', 'Medical News', 'Hospital Updates', 'Research']
        for cat_name in news_categories:
            NewsCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': cat_name.lower().replace(' ', '-')}
            )
        self.stdout.write(self.style.SUCCESS('Created news categories'))

        # Time Slots
        time_slots = [
            (time(9, 0), time(9, 30)),
            (time(9, 30), time(10, 0)),
            (time(10, 0), time(10, 30)),
            (time(10, 30), time(11, 0)),
            (time(11, 0), time(11, 30)),
            (time(11, 30), time(12, 0)),
            (time(14, 0), time(14, 30)),
            (time(14, 30), time(15, 0)),
            (time(15, 0), time(15, 30)),
            (time(15, 30), time(16, 0)),
            (time(16, 0), time(16, 30)),
            (time(16, 30), time(17, 0)),
        ]
        for start, end in time_slots:
            TimeSlot.objects.get_or_create(start_time=start, end_time=end)
        self.stdout.write(self.style.SUCCESS('Created time slots'))

        # FAQs
        faqs_data = [
            {
                'question': 'How do I book an appointment?',
                'answer': 'You can book an appointment online through our website or by calling our reception.'
            },
            {
                'question': 'What insurance do you accept?',
                'answer': 'We accept most major insurance providers. Please contact us to verify your coverage.'
            },
            {
                'question': 'What are your visiting hours?',
                'answer': 'Visiting hours are from 10:00 AM to 8:00 PM daily.'
            },
        ]
        for i, faq_data in enumerate(faqs_data):
            FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={'answer': faq_data['answer'], 'order': i}
            )
        self.stdout.write(self.style.SUCCESS('Created FAQs'))

        self.stdout.write(self.style.SUCCESS('Initial data setup complete!'))