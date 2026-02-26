# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import (
    HospitalSettings, HeroSlide, AboutSection, Feature,
    Testimonial, FAQ, ContactMessage, StaticPage
)
from .forms import ContactForm


def home(request):
    # Import here to avoid circular imports
    from doctors.models import DoctorProfile
    from services.models import Service
    from news.models import Article
    
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'about': AboutSection.objects.filter(is_active=True).first(),
        'features': Feature.objects.filter(is_active=True)[:6],
        'featured_doctors': DoctorProfile.objects.filter(is_active=True, is_featured=True)[:4],
        'featured_services': Service.objects.filter(is_active=True, is_featured=True)[:6],
        'latest_news': Article.objects.filter(status='published')[:3],
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'about': AboutSection.objects.filter(is_active=True).first(),
        'features': Feature.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'faqs': FAQ.objects.filter(is_active=True)[:10],
    }
    return render(request, 'core/contact.html', context)


def contact_ajax(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True,
                'message': 'Thank you for contacting us! We will get back to you soon.'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'core/faq.html', {'faqs': faqs})


def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, is_active=True)
    return render(request, 'core/static_page.html', {'page': page})


def privacy_policy(request):
    page = StaticPage.objects.filter(slug='privacy-policy', is_active=True).first()
    return render(request, 'core/static_page.html', {'page': page})


def terms_conditions(request):
    page = StaticPage.objects.filter(slug='terms-conditions', is_active=True).first()
    return render(request, 'core/static_page.html', {'page': page})