from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

from disasterinfosite import views

urlpatterns = [
   url(r'^admin/', admin.site.urls),
   url(r'^accounts/login/$', LoginView),
   url(r'^accounts/logout/$', LogoutView),
   url(r'^accounts/create_user/$', views.create_user),
   url(r'^accounts/update_profile/$', views.update_profile),
   url(r'^i18n/', include('django.conf.urls.i18n'))
]
# Recommend removing the prefix_default_language argument if you translate/localize this site.
urlpatterns += i18n_patterns(url(r'^$', views.app_view, name='index'), prefix_default_language=False)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
