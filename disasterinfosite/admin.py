from django.contrib.gis import admin
from embed_video.admin import AdminVideoMixin
from solo.admin import SingletonModelAdmin
######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminModelImports
from .models import EmbedSnugget, TextSnugget, SnuggetSection, SnuggetSubSection, Location, SiteSettings, SupplyKit, ImportantLink, EQ_Fault_Buffer, EQ_Historic_Distance, EQ_Most_Like, EQ_Worst_Case, Fire_Hist_Bound, Fire_Intensity, Fire_Worst_Case_placeholder, Flood_Channel_Migration_Zones, Flood_FEMA_DFRIM_2015, Flood_Worst_Case_ph, Landslide_placeholder
# END OF GENERATED CODE BLOCK
######################################################

admin.site.register(SnuggetSection, admin.ModelAdmin)
admin.site.register(SnuggetSubSection, admin.ModelAdmin)


class SnuggetAdmin(admin.ModelAdmin):
######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminLists
    list_display = ('shortname', 'section', 'sub_section', 'EQ_Fault_Buffer_filter', 'EQ_Historic_Distance_filter', 'EQ_Most_Like_filter', 'EQ_Worst_Case_filter', 'Fire_Hist_Bound_filter', 'Fire_Intensity_filter', 'Fire_Worst_Case_placeholder_filter', 'Flood_Channel_Migration_Zones_filter', 'Flood_FEMA_DFRIM_2015_filter', 'Flood_Worst_Case_ph_filter', 'Landslide_placeholder_filter')
    list_filter = ('section', 'sub_section', 'EQ_Fault_Buffer_filter', 'EQ_Historic_Distance_filter', 'EQ_Most_Like_filter', 'EQ_Worst_Case_filter', 'Fire_Hist_Bound_filter', 'Fire_Intensity_filter', 'Fire_Worst_Case_placeholder_filter', 'Flood_Channel_Migration_Zones_filter', 'Flood_FEMA_DFRIM_2015_filter', 'Flood_Worst_Case_ph_filter', 'Landslide_placeholder_filter')

    fieldsets = (
        (None, {
            'fields': ('section', 'sub_section')
        }),
        ('Filters', {
            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',
            'fields': (('EQ_Fault_Buffer_filter', 'EQ_Historic_Distance_filter', 'EQ_Most_Like_filter', 'EQ_Worst_Case_filter', 'Fire_Hist_Bound_filter', 'Fire_Intensity_filter', 'Fire_Worst_Case_placeholder_filter', 'Flood_Channel_Migration_Zones_filter', 'Flood_FEMA_DFRIM_2015_filter', 'Flood_Worst_Case_ph_filter', 'Landslide_placeholder_filter'))
        })
    )
# END OF GENERATED CODE BLOCK
######################################################

    def shortname(self, obj):
        return "Undefined"


class TextAdmin(SnuggetAdmin):
    fieldsets = SnuggetAdmin.fieldsets + ((None, {
        'fields': ('content',),
        }),
    )

    def shortname(self, obj):
        return 'Text: "' + str(obj) + '"'


class EmbedAdmin(AdminVideoMixin, SnuggetAdmin):
    fieldsets = SnuggetAdmin.fieldsets + ((None, {
        'fields': ('embed',),
        }),
    )

    def shortname(self, obj):
        return "EmbedSnugget"

admin.site.register(TextSnugget, TextAdmin)
admin.site.register(EmbedSnugget, EmbedAdmin)


class GeoNoEditAdmin(admin.GeoModelAdmin):
    modifiable = False

admin.site.register(ImportantLink, admin.ModelAdmin)
admin.site.register(SiteSettings, SingletonModelAdmin)
admin.site.register(Location, SingletonModelAdmin)
admin.site.register(SupplyKit, SingletonModelAdmin)

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminSiteRegistrations
admin.site.register(EQ_Fault_Buffer, GeoNoEditAdmin)
admin.site.register(EQ_Historic_Distance, GeoNoEditAdmin)
admin.site.register(EQ_Most_Like, GeoNoEditAdmin)
admin.site.register(EQ_Worst_Case, GeoNoEditAdmin)
admin.site.register(Fire_Hist_Bound, GeoNoEditAdmin)
admin.site.register(Fire_Intensity, GeoNoEditAdmin)
admin.site.register(Fire_Worst_Case_placeholder, GeoNoEditAdmin)
admin.site.register(Flood_Channel_Migration_Zones, GeoNoEditAdmin)
admin.site.register(Flood_FEMA_DFRIM_2015, GeoNoEditAdmin)
admin.site.register(Flood_Worst_Case_ph, GeoNoEditAdmin)
admin.site.register(Landslide_placeholder, GeoNoEditAdmin)
# END OF GENERATED CODE BLOCK
######################################################
