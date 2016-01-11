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
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsClasses
class EQ_Fault_Buffer(models.Model):
    snugget_id = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return str(self.snugget_id)

class EQ_GroundShaking_MostLike(models.Model):
    intensity = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return str(self.intensity)

class EQ_Historic_Distance(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return str(self.lookup_val)

class Fire_hist_nrocky_1889_2003_all(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return str(self.lookup_val)

class Flood_FEMA_DFIRM_2015(models.Model):
    femades = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return str(self.femades)

class MT_groundshaking(models.Model):
    intensity = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return str(self.intensity)

# END OF GENERATED CODE BLOCK
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
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsFilters
    EQ_Fault_Buffer_filter = models.ForeignKey(EQ_Fault_Buffer, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    EQ_GroundShaking_MostLike_filter = models.ForeignKey(EQ_GroundShaking_MostLike, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    EQ_Historic_Distance_filter = models.ForeignKey(EQ_Historic_Distance, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Fire_hist_nrocky_1889_2003_all_filter = models.ForeignKey(Fire_hist_nrocky_1889_2003_all, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Flood_FEMA_DFIRM_2015_filter = models.ForeignKey(Flood_FEMA_DFIRM_2015, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    MT_groundshaking_filter = models.ForeignKey(MT_groundshaking, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
# END OF GENERATED CODE BLOCK
######################################################

    section = models.ForeignKey(SnuggetSection, related_name='+', on_delete=models.PROTECT)
    sub_section = models.ForeignKey(SnuggetSubSection, related_name='+', on_delete=models.PROTECT, null=True, blank=True)
 
    def getRelatedTemplate(self):
        return "snugget.html"

    @staticmethod
    def findSnuggetsForPoint(lat=0, lng=0, merge_deform = True):
        pnt = Point(lng, lat)

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsGeoFilters
        qs_EQ_Fault_Buffer = EQ_Fault_Buffer.objects.filter(geom__contains=pnt)
        EQ_Fault_Buffer_rating = qs_EQ_Fault_Buffer.values_list('snugget_id', flat=True)
        EQ_Fault_Buffer_snuggets = Snugget.objects.filter(EQ_Fault_Buffer_filter__snugget_id__exact=EQ_Fault_Buffer_rating).select_subclasses()

        qs_EQ_GroundShaking_MostLike = EQ_GroundShaking_MostLike.objects.filter(geom__contains=pnt)
        EQ_GroundShaking_MostLike_rating = qs_EQ_GroundShaking_MostLike.values_list('intensity', flat=True)
        EQ_GroundShaking_MostLike_snuggets = Snugget.objects.filter(EQ_GroundShaking_MostLike_filter__intensity__exact=EQ_GroundShaking_MostLike_rating).select_subclasses()

        qs_EQ_Historic_Distance = EQ_Historic_Distance.objects.filter(geom__contains=pnt)
        EQ_Historic_Distance_rating = qs_EQ_Historic_Distance.values_list('lookup_val', flat=True)
        EQ_Historic_Distance_snuggets = Snugget.objects.filter(EQ_Historic_Distance_filter__lookup_val__exact=EQ_Historic_Distance_rating).select_subclasses()

        qs_Fire_hist_nrocky_1889_2003_all = Fire_hist_nrocky_1889_2003_all.objects.filter(geom__contains=pnt)
        Fire_hist_nrocky_1889_2003_all_rating = qs_Fire_hist_nrocky_1889_2003_all.values_list('lookup_val', flat=True)
        Fire_hist_nrocky_1889_2003_all_snuggets = Snugget.objects.filter(Fire_hist_nrocky_1889_2003_all_filter__lookup_val__exact=Fire_hist_nrocky_1889_2003_all_rating).select_subclasses()

        qs_Flood_FEMA_DFIRM_2015 = Flood_FEMA_DFIRM_2015.objects.filter(geom__contains=pnt)
        Flood_FEMA_DFIRM_2015_rating = qs_Flood_FEMA_DFIRM_2015.values_list('femades', flat=True)
        Flood_FEMA_DFIRM_2015_snuggets = Snugget.objects.filter(Flood_FEMA_DFIRM_2015_filter__femades__exact=Flood_FEMA_DFIRM_2015_rating).select_subclasses()

        qs_MT_groundshaking = MT_groundshaking.objects.filter(geom__contains=pnt)
        MT_groundshaking_rating = qs_MT_groundshaking.values_list('intensity', flat=True)
        MT_groundshaking_snuggets = Snugget.objects.filter(MT_groundshaking_filter__intensity__exact=MT_groundshaking_rating).select_subclasses()


        return {'groups': {
                          'EQ_Fault_Buffer_snugs': EQ_Fault_Buffer_snuggets,
                          'EQ_GroundShaking_MostLike_snugs': EQ_GroundShaking_MostLike_snuggets,
                          'EQ_Historic_Distance_snugs': EQ_Historic_Distance_snuggets,
                          'Fire_hist_nrocky_1889_2003_all_snugs': Fire_hist_nrocky_1889_2003_all_snuggets,
                          'Flood_FEMA_DFIRM_2015_snugs': Flood_FEMA_DFIRM_2015_snuggets,
                          'MT_groundshaking_snugs': MT_groundshaking_snuggets
                          },
                'EQ_Fault_Buffer_rating': EQ_Fault_Buffer_rating,
                'EQ_GroundShaking_MostLike_rating': EQ_GroundShaking_MostLike_rating,
                'EQ_Historic_Distance_rating': EQ_Historic_Distance_rating,
                'Fire_hist_nrocky_1889_2003_all_rating': Fire_hist_nrocky_1889_2003_all_rating,
                'Flood_FEMA_DFIRM_2015_rating': Flood_FEMA_DFIRM_2015_rating,
                'MT_groundshaking_rating': MT_groundshaking_rating
                }
# END OF GENERATED CODE BLOCK
######################################################



    def __str__(self):
        return "Snugget base class string."


class TextSnugget(Snugget):
    name = SNUGGET_TYPES[SNUG_TEXT]
    content = models.TextField()
    heading = models.TextField(default="")
    image = models.TextField(default="")
    percentage = models.FloatField(null=True)

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
