# core/context_processors.py

from .models import HospitalSettings, StaticPage


def hospital_settings(request):
    settings = HospitalSettings.get_settings()
    footer_pages = StaticPage.objects.filter(is_active=True, show_in_footer=True)
    
    return {
        'hospital': settings,
        'footer_pages': footer_pages,
    }