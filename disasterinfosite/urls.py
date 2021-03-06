from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.gis import admin
from django.conf import settings

from disasterinfosite import views

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^i18n/', include('django.conf.urls.i18n')),
  # API urls
  url(r'^accounts/login/$', views.login_view, name="login"),
  url(r'^accounts/logout/$', views.logout_view, name="logout"),
  url(r'^accounts/create_user/$', views.create_user, name="create_user"),
  url(r'^accounts/update_profile/$', views.update_profile, name="update_profile"),
  url(r'^accounts/update_prepare_action/$', views.prepare_action_update, name='prepare_action_update')
]

# user-facing URLs
urlpatterns += i18n_patterns(url(r'^$', views.app_view, name='index'))
urlpatterns += i18n_patterns(url(r'^about/$', views.about_view, name='about'))
urlpatterns += i18n_patterns(url(r'^prepare/$', views.prepare_view, name='prepare'))

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)