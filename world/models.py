from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from embed_video.fields import EmbedVideoField
from model_utils.managers import InheritanceManager
from solo.models import SingletonModel

SNUG_TEXT = 0
SNUG_AUDIO = 1
SNUG_VID = 2

SNUGGET_TYPES = (
                 ('SNUG_TEXT', 'TextSnugget'),
                 )

class SiteSettings(SingletonModel):
    """A singleton model to represent site-wide settings."""
    about_text = models.TextField(
        default="Information about your organization goes here.",
        help_text="Describe the data and the agencies that it came from."
    )
    contact_email = models.EmailField(
        default="contact@youremail.com",
        help_text="Put a contact email for the maintainer of this site here."
    )
    site_url = models.URLField(
        default="http://www.example.com",
        help_text="Put the URL to this site here."
    )
    site_title = models.CharField(
        max_length=50,
        default="Your Title Here!"
    )
    site_description = models.CharField(
        max_length=200,
        default="A disaster preparedness website",
        help_text="A small, catchy description for this site."
    )

    def __unicode__(self):
        return u"Site Settings"

    class Meta:
        verbose_name = "Site Settings"


class Location(SingletonModel):
    """A singleton model to represent the location covered by this website's data"""
    area_name = models.CharField(
        max_length=100,
        default="the affected area",
        help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'."
    )
    disaster_name = models.CharField(
        max_length=50,
        default="some disaster",
        help_text="Something like 'a tsunami', 'an earthquake', 'a fire'"
    )
    disaster_description = models.TextField(
        default="A natural disaster could strike your area at any time.", 
        help_text="A description of what we are trying to help people prepare for."
    )
    evacuation_routes_link = models.URLField(
        default="",
        blank=True,
        help_text="A link to website that can help people find an evacuation route"
    )
    emergency_management_link = models.URLField(
        default="http://www.fema.gov",
        help_text="A link to your local office of emergency management."
    )
    
    def __unicode__(self):
        return u"Location Information"

    class Meta:
        verbose_name = "Location Information"
      
######################################################
# Insert generated modelsClasses here
######################################################
        
 
class RecoveryLevels(models.Model):
    name = models.CharField(max_length=50)
    shortLabel = models.CharField(max_length=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class Infrastructure(models.Model):
    name = models.CharField(max_length=255)
    eventOccursRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    firstDayRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    threeDaysRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    sevenDaysRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    fourWeeksRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    threeMonthsRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    sixMonthsRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    twelveMonthsRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    threeYearsRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
    threePlusYearsRecovery = models.ForeignKey(RecoveryLevels, related_name='+', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name + " in " + str(self.zone)


class InfrastructureGroup(models.Model):
    name = models.CharField(max_length=50)
    items = models.ManyToManyField(Infrastructure)

    def __str__(self):
        return self.name


class InfrastructureCategory(models.Model):
    name = models.CharField(max_length=50)
    groups = models.ManyToManyField(InfrastructureGroup)

    def __str__(self):
        return self.name + " in " + str(self.zone)


class SnuggetType(models.Model):
    name = models.CharField(max_length=50)
    model_name = models.CharField(max_length=255, choices=SNUGGET_TYPES)

    def __str__(self):
        return self.name


class SnuggetSection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SnuggetSubSection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Snugget(models.Model):
    objects = InheritanceManager()
######################################################
# Insert generated modelsFilters here
######################################################

    section = models.ForeignKey(SnuggetSection, related_name='+', on_delete=models.PROTECT)
    sub_section = models.ForeignKey(SnuggetSubSection, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
 
    def getRelatedTemplate(self):
        return "snugget.html"

    @staticmethod
    def findSnuggetsForPoint(lat=0, lng=0, merge_deform = True):
        pnt = Point(lng, lat)
######################################################
# Insert generated modelsGeoFilters here
######################################################


######################################################
# Insert generated modelsSnuggetReturns here
######################################################


    def __str__(self):
        return "Snugget base class string."


class TextSnugget(Snugget):
    name = SNUGGET_TYPES[SNUG_TEXT]
    content = models.TextField()

    def getRelatedTemplate(self):
        return "snugget_text.html"

    def __str__(self):
        return str(self.content)[:100]


class EmbedSnugget(Snugget):
    embed = EmbedVideoField()

    def getRelatedTemplate(self):
        return "snugget_embed.html"

    def __str__(self):
        return "Embed Snugget: " + str(self.embed)
