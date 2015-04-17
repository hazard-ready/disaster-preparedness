from django.contrib.gis import admin
from .models import *

admin.site.register(TsunamiZone, admin.GeoModelAdmin)
admin.site.register(ImpactZoneData, admin.GeoModelAdmin)
admin.site.register(ExpectedGroundShaking, admin.GeoModelAdmin)
admin.site.register(ImpactZone, admin.GeoModelAdmin)
admin.site.register(SnuggetType, admin.ModelAdmin)
admin.site.register(SnuggetSection, admin.ModelAdmin)
admin.site.register(SnuggetSubSection, admin.ModelAdmin)
admin.site.register(TextSnugget, admin.ModelAdmin)

# Maybe in the future
# admin.site.register(InfrastructureGroup, admin.ModelAdmin)
# admin.site.register(Infrastructure, admin.ModelAdmin)
# admin.site.register(InfrastructureCategory, admin.ModelAdmin)
# admin.site.register(RecoveryLevels, admin.ModelAdmin)
