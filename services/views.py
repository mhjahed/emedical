# services/views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Service, ServiceCategory


def services_list(request):
    """List all services"""
    services = Service.objects.filter(is_active=True).select_related('category')
    categories = ServiceCategory.objects.filter(is_active=True)
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        services = services.filter(category__slug=category_filter)
    
    paginator = Paginator(services, 12)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    
    context = {
        'services': services,
        'categories': categories,
        'category_filter': category_filter,
        'featured_services': Service.objects.filter(is_active=True, is_featured=True)[:4],
    }
    return render(request, 'services/services_list.html', context)


def service_detail(request, slug):
    """Service detail page"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Related services
    related_services = Service.objects.filter(
        is_active=True,
        category=service.category
    ).exclude(id=service.id)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
        'gallery_images': service.gallery_images.all(),
        'faqs': service.faqs.all(),
        'related_doctors': service.related_doctors.filter(is_active=True)[:4],
    }
    return render(request, 'services/service_detail.html', context)


def category_services(request, slug):
    """Services by category"""
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    services = Service.objects.filter(is_active=True, category=category)
    
    paginator = Paginator(services, 12)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    
    return render(request, 'services/category_services.html', {
        'category': category,
        'services': services
    })