from django.conf.urls import patterns, include, url
from django.contrib.gis import admin
from world import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cascadiaprepared.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'(?i)^zoneCheck', views.zoneCheck),   
    url(r'^admin/', include(admin.site.urls)),
)
