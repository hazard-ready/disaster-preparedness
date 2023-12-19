from .models import SiteSettings

def global_site_settings(request):
    return {
        'settings': SiteSettings.get_solo(),
    }
