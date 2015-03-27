from django.contrib.gis import admin
from .models import *

admin.site.register(TsunamiZone, admin.GeoModelAdmin)
admin.site.register(ImpactZoneData, admin.GeoModelAdmin)
admin.site.register(ExpectedGroundShaking, admin.GeoModelAdmin)
admin.site.register(InfrastructureGroup, admin.GeoModelAdmin)
admin.site.register(Infrastructure, admin.GeoModelAdmin)
admin.site.register(InfrastructureCategory, admin.GeoModelAdmin)
admin.site.register(RecoveryLevels, admin.GeoModelAdmin)
admin.site.register(ImpactZone, admin.GeoModelAdmin)
admin.site.register(Snugget, admin.GeoModelAdmin)
admin.site.register(SnuggetType, admin.GeoModelAdmin)
admin.site.register(SnuggetSection, admin.GeoModelAdmin)