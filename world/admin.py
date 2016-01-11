from django.contrib.gis import admin
from embed_video.admin import AdminVideoMixin
from solo.admin import SingletonModelAdmin
######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminModelImports
from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, RecoveryLevels, Location, SiteSettings, EQ_Fault_Buffer, EQ_GroundShaking_MostLike, EQ_Historic_Distance, Fire_hist_nrocky_1889_2003_all, Flood_FEMA_DFIRM_2015, MT_groundshaking
# END OF GENERATED CODE BLOCK
######################################################

admin.site.register(SnuggetSection, admin.ModelAdmin)
admin.site.register(SnuggetSubSection, admin.ModelAdmin)


class SnuggetAdmin(admin.ModelAdmin):
######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminLists
    list_display = ('shortname', 'section', 'sub_section', 'EQ_Fault_Buffer_filter', 'EQ_GroundShaking_MostLike_filter', 'EQ_Historic_Distance_filter', 'Fire_hist_nrocky_1889_2003_all_filter', 'Flood_FEMA_DFIRM_2015_filter', 'MT_groundshaking_filter')
    list_filter = ('section', 'sub_section', 'EQ_Fault_Buffer_filter', 'EQ_GroundShaking_MostLike_filter', 'EQ_Historic_Distance_filter', 'Fire_hist_nrocky_1889_2003_all_filter', 'Flood_FEMA_DFIRM_2015_filter', 'MT_groundshaking_filter')

    fieldsets = (
        (None, {
            'fields': ('section', 'sub_section')
        }),
        ('Filters', {
            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',
            'fields': (('EQ_Fault_Buffer_filter', 'EQ_GroundShaking_MostLike_filter', 'EQ_Historic_Distance_filter', 'Fire_hist_nrocky_1889_2003_all_filter', 'Flood_FEMA_DFIRM_2015_filter', 'MT_groundshaking_filter'))
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

admin.site.register(RecoveryLevels, admin.ModelAdmin)

# To make the UI more general
admin.site.register(SiteSettings, SingletonModelAdmin)
admin.site.register(Location, SingletonModelAdmin)

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminSiteRegistrations
admin.site.register(EQ_Fault_Buffer, GeoNoEditAdmin)
admin.site.register(EQ_GroundShaking_MostLike, GeoNoEditAdmin)
admin.site.register(EQ_Historic_Distance, GeoNoEditAdmin)
admin.site.register(Fire_hist_nrocky_1889_2003_all, GeoNoEditAdmin)
admin.site.register(Flood_FEMA_DFIRM_2015, GeoNoEditAdmin)
admin.site.register(MT_groundshaking, GeoNoEditAdmin)
# END OF GENERATED CODE BLOCK
######################################################
