from django.contrib.gis import admin
from embed_video.admin import AdminVideoMixin
from solo.admin import SingletonModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminModelImports
from .models import EmbedSnugget, TextSnugget, SnuggetSection, Location, SiteSettings, SupplyKit, ImportantLink, RDPOLiquefact_Clark, RDPO_counties, RDPOLiquefaction_OR, RDPOCascadiaM9_3_Clark, RDPO_region, RDPOCascadiaM9_OR
# END OF GENERATED CODE BLOCK
######################################################
from .models import ShapefileGroup, PastEventsPhoto, DataOverviewImage, UserProfile
from .actions import export_as_csv_action
# To turn translation on from modeltranslation.admin import TranslationAdmin

# To use translatable models and see them in DjangoAdmin, use the following 5 lines instead.
# admin.site.register(SnuggetSection, TranslationAdmin)
# admin.site.register(SnuggetSubSection, TranslationAdmin)
# admin.site.register(ShapefileGroup, TranslationAdmin)
# admin.site.register(PastEventsPhoto, TranslationAdmin)
# admin.site.register(DataOverviewImage, TranslationAdmin)

# Use the next three lines if you don't want to translate these models into other languages in Django Admin.
admin.site.register(SnuggetSection, admin.ModelAdmin)
admin.site.register(ShapefileGroup, admin.ModelAdmin)
admin.site.register(PastEventsPhoto, admin.ModelAdmin)
admin.site.register(DataOverviewImage, admin.ModelAdmin)


class SnuggetAdmin(admin.ModelAdmin):
######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminLists
    list_display = ('shortname', 'section', 'RDPOLiquefact_Clark_filter', 'RDPO_counties_filter', 'RDPOLiquefaction_OR_filter', 'RDPOCascadiaM9_3_Clark_filter', 'RDPO_region_filter', 'RDPOCascadiaM9_OR_filter')
    list_filter = ('section', 'RDPOLiquefact_Clark_filter', 'RDPO_counties_filter', 'RDPOLiquefaction_OR_filter', 'RDPOCascadiaM9_3_Clark_filter', 'RDPO_region_filter', 'RDPOCascadiaM9_OR_filter')

    fieldsets = (
        (None, {
            'fields': ('section',)
        }),
        ('Filters', {
            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',
            'fields': (('RDPOLiquefact_Clark_filter', 'RDPO_counties_filter', 'RDPOLiquefaction_OR_filter', 'RDPOCascadiaM9_3_Clark_filter', 'RDPO_region_filter', 'RDPOCascadiaM9_OR_filter'))
        })
    )
# END OF GENERATED CODE BLOCK
######################################################

    def shortname(self, obj):
        return "Undefined"


# if you want to translate text snuggets: class TextAdmin(SnuggetAdmin, TranslationAdmin):
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

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Users'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    actions = [export_as_csv_action("CSV Export", fields=('username','address1','address2','city','state','zip_code'))]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class GeoNoEditAdmin(admin.GeoModelAdmin):
    modifiable = False

# Uncomment the next lines if you want to translate fields in DjangoAdmin to different languages.
# admin.site.register(ImportantLink, TranslationAdmin)
# class SiteSettingsAdmin(SingletonModelAdmin, TranslationAdmin):
#     pass
# admin.site.register(SiteSettings, SiteSettingsAdmin)

# class LocationAdmin(SingletonModelAdmin, TranslationAdmin):
#     pass
# admin.site.register(Location, LocationAdmin)

# class SupplyKitAdmin(SingletonModelAdmin, TranslationAdmin):
#     pass
# admin.site.register(SupplyKit, SupplyKitAdmin)

# Keep this block as-is if you don't want to translate these models into other languages in DjangoAdmin.
admin.site.register(ImportantLink, admin.ModelAdmin)
admin.site.register(SiteSettings, SingletonModelAdmin)
admin.site.register(Location, SingletonModelAdmin)
admin.site.register(SupplyKit, SingletonModelAdmin)

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminSiteRegistrations
admin.site.register(RDPOLiquefact_Clark, GeoNoEditAdmin)
admin.site.register(RDPO_counties, GeoNoEditAdmin)
admin.site.register(RDPOLiquefaction_OR, GeoNoEditAdmin)
admin.site.register(RDPOCascadiaM9_3_Clark, GeoNoEditAdmin)
admin.site.register(RDPO_region, GeoNoEditAdmin)
admin.site.register(RDPOCascadiaM9_OR, GeoNoEditAdmin)
# END OF GENERATED CODE BLOCK
######################################################
