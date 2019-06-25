from django.contrib.gis import admin
from embed_video.admin import AdminVideoMixin
from solo.admin import SingletonModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminModelImports
from .models import EmbedSnugget, TextSnugget, SnuggetSection, Location, SiteSettings, RDPO_region_quake, RDPO_region_winter, RDPO_Lsd_Clark, RDPO_counties_quake, RDPOflood_OR, RDPO_counties_volcano, RDPO_Lsld_OR, RDPOFire_Clark, RDPO_region_summer, RDPO_region_fire, RDPOCascadiaM9_3_Clark, RDPOFire_OR, RDPO_region_volcano, RDPOLiquefaction_OR, RDPOCascadiaM9_Col, RDPOflood_clark, RDPO_region_flood, RDPOvolcanoes, RDPO_counties_winter, RDPO_counties_fire, RDPO_WA, RDPO_counties_flood, RDPO_OR, RDPOCascadiaM9_3Cnty, RDPO_region_slide, RDPOCascadiaM9_OR, RDPOLiquefact_Clark, RDPO_counties_summer, RDPOhistflood, RDPO_counties_slide
# END OF GENERATED CODE BLOCK
######################################################
from .models import ShapefileGroup, PastEventsPhoto, DataOverviewImage, UserProfile, PreparednessAction, SurveyCode
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
    list_display = ('shortname', 'section', 'RDPO_region_quake_filter', 'RDPO_region_winter_filter', 'RDPO_Lsd_Clark_filter', 'RDPO_counties_quake_filter', 'RDPOflood_OR_filter', 'RDPO_counties_volcano_filter', 'RDPO_Lsld_OR_filter', 'RDPOFire_Clark_filter', 'RDPO_region_summer_filter', 'RDPO_region_fire_filter', 'RDPOCascadiaM9_3_Clark_filter', 'RDPOFire_OR_filter', 'RDPO_region_volcano_filter', 'RDPOLiquefaction_OR_filter', 'RDPOCascadiaM9_Col_filter', 'RDPOflood_clark_filter', 'RDPO_region_flood_filter', 'RDPOvolcanoes_filter', 'RDPO_counties_winter_filter', 'RDPO_counties_fire_filter', 'RDPO_WA_filter', 'RDPO_counties_flood_filter', 'RDPO_OR_filter', 'RDPOCascadiaM9_3Cnty_filter', 'RDPO_region_slide_filter', 'RDPOCascadiaM9_OR_filter', 'RDPOLiquefact_Clark_filter', 'RDPO_counties_summer_filter', 'RDPOhistflood_filter', 'RDPO_counties_slide_filter')
    list_filter = ('section', 'RDPO_region_quake_filter', 'RDPO_region_winter_filter', 'RDPO_Lsd_Clark_filter', 'RDPO_counties_quake_filter', 'RDPOflood_OR_filter', 'RDPO_counties_volcano_filter', 'RDPO_Lsld_OR_filter', 'RDPO_region_fire_filter', 'RDPOCascadiaM9_3_Clark_filter', 'RDPOFire_OR_filter', 'RDPO_region_volcano_filter', 'RDPOLiquefaction_OR_filter', 'RDPOCascadiaM9_Col_filter', 'RDPOflood_clark_filter', 'RDPO_region_flood_filter', 'RDPOvolcanoes_filter', 'RDPO_counties_winter_filter', 'RDPO_counties_fire_filter', 'RDPO_WA_filter', 'RDPO_counties_flood_filter', 'RDPO_OR_filter', 'RDPOCascadiaM9_3Cnty_filter', 'RDPO_region_slide_filter', 'RDPOCascadiaM9_OR_filter', 'RDPOLiquefact_Clark_filter', 'RDPO_counties_summer_filter', 'RDPOhistflood_filter', 'RDPO_counties_slide_filter')

    fieldsets = (
        (None, {
            'fields': ('section',)
        }),
        ('Filters', {
            'description': 'Choose a filter value this snugget will show up for.  It is recommended you only select a value for one filter and leave the rest empty.',
            'fields': (('RDPO_region_quake_filter', 'RDPO_region_winter_filter', 'RDPO_Lsd_Clark_filter', 'RDPO_counties_quake_filter', 'RDPOflood_OR_filter', 'RDPO_counties_volcano_filter', 'RDPO_Lsld_OR_filter', 'RDPOFire_Clark_filter', 'RDPO_region_summer_filter', 'RDPO_region_fire_filter', 'RDPOCascadiaM9_3_Clark_filter', 'RDPOFire_OR_filter', 'RDPO_region_volcano_filter', 'RDPOLiquefaction_OR_filter', 'RDPOCascadiaM9_Col_filter', 'RDPOflood_clark_filter', 'RDPO_region_flood_filter', 'RDPOvolcanoes_filter', 'RDPO_counties_winter_filter', 'RDPO_counties_fire_filter', 'RDPO_WA_filter', 'RDPO_counties_flood_filter', 'RDPO_OR_filter', 'RDPOCascadiaM9_3Cnty_filter', 'RDPO_region_slide_filter', 'RDPOCascadiaM9_OR_filter', 'RDPOLiquefact_Clark_filter', 'RDPO_counties_summer_filter', 'RDPOhistflood_filter', 'RDPO_counties_slide_filter'))
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
    actions = [export_as_csv_action("CSV Export", fields=('username','address1','address2','city','state','zip_code'), model=UserProfile)]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Make the entered survey codes exportable as a CSV
class SurveyCodeAdmin(admin.ModelAdmin):
    model = SurveyCode
    actions = [export_as_csv_action("CSV Export", fields=('code',))]

admin.site.register(SurveyCode, SurveyCodeAdmin)


class GeoNoEditAdmin(admin.GeoModelAdmin):
    modifiable = False

# Uncomment the next lines if you want to translate fields in DjangoAdmin to different languages.
# class SiteSettingsAdmin(SingletonModelAdmin, TranslationAdmin):
#     pass
# admin.site.register(SiteSettings, SiteSettingsAdmin)

# class LocationAdmin(SingletonModelAdmin, TranslationAdmin):
#     pass
# admin.site.register(Location, LocationAdmin)


# Keep this block as-is if you don't want to translate these models into other languages in DjangoAdmin.
admin.site.register(SiteSettings, SingletonModelAdmin)
admin.site.register(Location, SingletonModelAdmin)

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# adminSiteRegistrations
admin.site.register(RDPO_region_quake, GeoNoEditAdmin)
admin.site.register(RDPO_region_winter, GeoNoEditAdmin)
admin.site.register(RDPO_Lsd_Clark, GeoNoEditAdmin)
admin.site.register(RDPO_counties_quake, GeoNoEditAdmin)
admin.site.register(RDPOflood_OR, GeoNoEditAdmin)
admin.site.register(RDPO_counties_volcano, GeoNoEditAdmin)
admin.site.register(RDPO_Lsld_OR, GeoNoEditAdmin)
admin.site.register(RDPOFire_Clark, GeoNoEditAdmin)
admin.site.register(RDPO_region_summer, GeoNoEditAdmin)
admin.site.register(RDPO_region_fire, GeoNoEditAdmin)
admin.site.register(RDPOCascadiaM9_3_Clark, GeoNoEditAdmin)
admin.site.register(RDPOFire_OR, GeoNoEditAdmin)
admin.site.register(RDPO_region_volcano, GeoNoEditAdmin)
admin.site.register(RDPOLiquefaction_OR, GeoNoEditAdmin)
admin.site.register(RDPOCascadiaM9_Col, GeoNoEditAdmin)
admin.site.register(RDPOflood_clark, GeoNoEditAdmin)
admin.site.register(RDPO_region_flood, GeoNoEditAdmin)
admin.site.register(RDPOvolcanoes, GeoNoEditAdmin)
admin.site.register(RDPO_counties_winter, GeoNoEditAdmin)
admin.site.register(RDPO_counties_fire, GeoNoEditAdmin)
admin.site.register(RDPO_WA, GeoNoEditAdmin)
admin.site.register(RDPO_counties_flood, GeoNoEditAdmin)
admin.site.register(RDPO_OR, GeoNoEditAdmin)
admin.site.register(RDPOCascadiaM9_3Cnty, GeoNoEditAdmin)
admin.site.register(RDPO_region_slide, GeoNoEditAdmin)
admin.site.register(RDPOCascadiaM9_OR, GeoNoEditAdmin)
admin.site.register(RDPOLiquefact_Clark, GeoNoEditAdmin)
admin.site.register(RDPO_counties_summer, GeoNoEditAdmin)
admin.site.register(RDPOhistflood, GeoNoEditAdmin)
admin.site.register(RDPO_counties_slide, GeoNoEditAdmin)
# END OF GENERATED CODE BLOCK
######################################################
