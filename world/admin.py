from django.contrib.gis import admin
from .models import *

admin.site.register(TsunamiZone, admin.GeoModelAdmin)
admin.site.register(ImpactZone, admin.GeoModelAdmin)
admin.site.register(ExpectedGroundShaking, admin.GeoModelAdmin)