from django.contrib.gis import admin
from .models import TsunamiZone
from .models import WorldBorder

admin.site.register(TsunamiZone, admin.GeoModelAdmin)
admin.site.register(WorldBorder, admin.GeoModelAdmin)