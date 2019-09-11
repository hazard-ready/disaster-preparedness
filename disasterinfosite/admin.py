from django.contrib.gis import admin
from solo.admin import SingletonModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import SnuggetSection, SiteSettings, ShapefileGroup, PastEventsPhoto, DataOverviewImage, UserProfile, SurveyCode
from .actions import export_as_csv_action
from modeltranslation.admin import TranslationAdmin

# To use translatable models and see them in DjangoAdmin, use the following 5 lines instead.
admin.site.register(SnuggetSection, TranslationAdmin)
admin.site.register(ShapefileGroup, TranslationAdmin)
admin.site.register(PastEventsPhoto, TranslationAdmin)
admin.site.register(DataOverviewImage, TranslationAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Users'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    actions = [export_as_csv_action("CSV Export", fields=('username','address1','address2','city','state','zip_code', 'actions_taken'), model=UserProfile)]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Make the entered survey codes exportable as a CSV
class SurveyCodeAdmin(admin.ModelAdmin):
    model = SurveyCode
    actions = [export_as_csv_action("CSV Export", fields=('code', 'dateEntered'))]

admin.site.register(SurveyCode, SurveyCodeAdmin)


class GeoNoEditAdmin(admin.GeoModelAdmin):
    modifiable = False


# Uncomment the next lines if you want to translate fields in DjangoAdmin to different languages.
class SiteSettingsAdmin(SingletonModelAdmin, TranslationAdmin):
    pass
admin.site.register(SiteSettings, SiteSettingsAdmin)

