from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from django.conf import settings

from world import views

urlpatterns = patterns('',
    url(r'^$', views.app_view),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )