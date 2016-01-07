from django.contrib.gis import admin
from embed_video.admin import AdminVideoMixin
from solo.admin import SingletonModelAdmin
######################################################
# Replace the next line with generated adminModelImports
from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, RecoveryLevels, Location, SiteSettings, EQ_GroundShaking_MostLike, Flood_FEMA_DFIRM_2015, MT_groundshaking

######################################################

admin.site.register(SnuggetSection, admin.ModelAdmin)
admin.site.register(SnuggetSubSection, admin.ModelAdmin)


class SnuggetAdmin(admin.ModelAdmin):
######################################################
# Insert generated adminLists here
######################################################
    list_display = ('shortname', 'section', 'sub_section', 'EQ_GroundShaking_MostLike_filter', 'Flood_FEMA_DFIRM_2015_filter', 'MT_groundshaking_filter')
    list_filter = ('section', 'sub_section', 'EQ_GroundShaking_MostLike_filter', 'Flood_FEMA_DFIRM_2015_filter', 'MT_groundshaking_filter')

    fieldsets = (
        (None, {
            'fields': ('section', 'sub_section')
        }),
        ('Filters', {
            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',
            'fields': (('EQ_GroundShaking_MostLike_filter', 'Flood_FEMA_DFIRM_2015_filter', 'MT_groundshaking_filter'))
        })
    )

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
# Insert generated adminSiteRegistrations here
######################################################
admin.site.register(EQ_GroundShaking_MostLike, GeoNoEditAdmin)
admin.site.register(Flood_FEMA_DFIRM_2015, GeoNoEditAdmin)
admin.site.register(MT_groundshaking, GeoNoEditAdmin)



