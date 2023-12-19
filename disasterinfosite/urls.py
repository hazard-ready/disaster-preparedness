from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.gis import admin
from django.conf import settings

from disasterinfosite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    # API urls
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create_user/', views.create_user, name="create_user"),

    # Our own user account actions
    path('accounts/update_profile/', views.update_profile, name="update_profile"),
    path('accounts/update_prepare_action/',
         views.prepare_action_update, name='prepare_action_update')
]

# user-facing URLs
urlpatterns += i18n_patterns(path('', views.app_view, name='index'))
urlpatterns += i18n_patterns(path('about/', views.about_view, name='about'))
urlpatterns += i18n_patterns(path('prepare/',
                                  views.prepare_view, name='prepare'))
urlpatterns += i18n_patterns(path('data/', views.data_view, name='data'))

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
