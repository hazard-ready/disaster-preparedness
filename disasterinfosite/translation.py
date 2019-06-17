# Uncomment if you want to translate Django models.

from modeltranslation.translator import register, translator, TranslationOptions
from .models import SiteSettings, Location, ShapefileGroup, PastEventsPhoto, DataOverviewImage, TextSnugget, EmbedSnugget, SlideshowSnugget, SnuggetPopOut, SnuggetSection

@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('about_text', 'site_title', 'site_description', 'intro_text', 'who_made_this')

@register(Location)
class LocationTranslationOptions(TranslationOptions):
  fields = ('area_name', 'community_leaders')

@register(ShapefileGroup)
class ShapefileGroupTranslationOptions(TranslationOptions):
  fields = ('display_name',)

@register(PastEventsPhoto)
class PastEventsPhotoTranslationOptions(TranslationOptions):
  fields = ('caption',)

@register(DataOverviewImage)
class DataOverviewImageTranslationOptions(TranslationOptions):
  fields = ('link_text',)

@register(TextSnugget)
class TextSnuggetTranslationOptions(TranslationOptions):
  fields = ('content',)

@register(EmbedSnugget)
class EmbedSnuggetTranslationOptions(TranslationOptions):
  fields = ('text',)

@register(SlideshowSnugget)
class SlideshowSnuggetTranslationOptions(TranslationOptions):
  fields = ('text',)

@register(SnuggetPopOut)
class SnuggetPopOutTranslationOptions(TranslationOptions):
  fields = ('text', 'alt_text')

@register(SnuggetSection)
class SnuggetSectionTranslationOptions(TranslationOptions):
  fields = ('display_name',)
