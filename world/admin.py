from django.contrib.gis import admin
from embed_video.admin import AdminVideoMixin
from .models import *

admin.site.register(TsunamiZone, admin.GeoModelAdmin)
admin.site.register(ImpactZoneData, admin.GeoModelAdmin)
admin.site.register(ExpectedGroundShaking, admin.GeoModelAdmin)
admin.site.register(ImpactZone, admin.GeoModelAdmin)
admin.site.register(SnuggetSection, admin.ModelAdmin)
admin.site.register(SnuggetSubSection, admin.ModelAdmin)

class SnuggetAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'shaking_filter', 'impact_zone_filter', 'tsunami_filter', 'liquifaction_filter', 'landslide_filter', 'section', 'sub_section')
    list_filter = ('shaking_filter', 'impact_zone_filter', 'tsunami_filter', 'liquifaction_filter', 'landslide_filter', 'section', 'sub_section')
    
    fieldsets = (
        (None, {
           'fields': ('section', 'sub_section'),
        }),
        ('Filters', {
            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',
            'fields': (('shaking_filter', 'impact_zone_filter', 'tsunami_filter', 'liquifaction_filter', 'landslide_filter'),)
        }),
    )    
    
    def shortname(self, obj):
        return "Undefined";

class TextAdmin(SnuggetAdmin):
    fieldsets = SnuggetAdmin.fieldsets + ((None, {
            'fields': ('content',),
        }),
    )
    
    def shortname(self, obj):
        return 'Text: "' + str(obj) + '"';
    
class EmbedAdmin(AdminVideoMixin, SnuggetAdmin):    
    fieldsets = SnuggetAdmin.fieldsets + ((None, {
            'fields': ('embed',),
        }),
    )
    
    def shortname(self, obj):
        return "EmbedSnugget";
    
admin.site.register(TextSnugget, TextAdmin)
admin.site.register(EmbedSnugget, EmbedAdmin)

# Maybe in the future
# admin.site.register(InfrastructureGroup, admin.ModelAdmin)
# admin.site.register(Infrastructure, admin.ModelAdmin)
# admin.site.register(InfrastructureCategory, admin.ModelAdmin)
# admin.site.register(RecoveryLevels, admin.ModelAdmin)
