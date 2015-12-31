from django.contrib.gis import admin
from embed_video.admin import AdminVideoMixin
from solo.admin import SingletonModelAdmin
######################################################
# Replace the next line with generated adminModelImports
from .models import TextSnugget, EmbedSnugget, SnuggetSection, SnuggetSubSection, Infrastructure, InfrastructureGroup, InfrastructureCategory, RecoveryLevels, Location, SiteSettings
######################################################

admin.site.register(SnuggetSection, admin.ModelAdmin)
admin.site.register(SnuggetSubSection, admin.ModelAdmin)


class SnuggetAdmin(admin.ModelAdmin):
######################################################
# Insert generated adminLists here
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

# Maybe in the future
admin.site.register(InfrastructureGroup, admin.ModelAdmin)
admin.site.register(Infrastructure, admin.ModelAdmin)
admin.site.register(InfrastructureCategory, admin.ModelAdmin)
admin.site.register(RecoveryLevels, admin.ModelAdmin)

# To make the UI more general
admin.site.register(SiteSettings, SingletonModelAdmin)
admin.site.register(Location, SingletonModelAdmin)

######################################################
# Insert generated adminSiteRegistrations here
######################################################

