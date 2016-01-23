
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import Extent
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
        blank=True,
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
    intro_text= models.TextField(
        default="A natural disaster could strike your area at any time.",
        help_text="A description of what we are trying to help people prepare for, or the goal of your site."
    )
    who_made_this = models.TextField(
        default="Information about the creators and maintainers of this particular site.",
        help_text="Include information about who you are and how to contact you."
    )
    data_download = models.URLField(
        blank=True,
        help_text="A link where people can download a zipfile of all the data that powers this site."
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

    community_leaders = models.TextField(
        default="Information about community leaders goes here.",
        help_text="Information about community leaders, how to contact them, and form groups."
    )

    def __unicode__(self):
        return u"Location Information"

    @staticmethod
    def get_data_bounds():
        bounds = {
    ######################################################
    # GENERATED CODE GOES HERE
    # DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
    # locationsList
            'EQ_Fault_Buffer': EQ_Fault_Buffer.objects.data_bounds(),
            'EQ_Historic_Distance': EQ_Historic_Distance.objects.data_bounds(),
            'EQ_Most_Like': EQ_Most_Like.objects.data_bounds(),
            'EQ_Worst_Case': EQ_Worst_Case.objects.data_bounds(),
            'Fire_Hist_Bound': Fire_Hist_Bound.objects.data_bounds(),
            'Fire_Intensity': Fire_Intensity.objects.data_bounds(),
            'Fire_Worst_Case_placeholder': Fire_Worst_Case_placeholder.objects.data_bounds(),
            'Flood_Channel_Migration_Zones': Flood_Channel_Migration_Zones.objects.data_bounds(),
            'Flood_FEMA_DFRIM_2015': Flood_FEMA_DFRIM_2015.objects.data_bounds(),
            'Flood_Worst_Case_ph': Flood_Worst_Case_ph.objects.data_bounds(),
            'Landslide_placeholder': Landslide_placeholder.objects.data_bounds()
    # END OF GENERATED CODE BLOCK
    ######################################################
        }

        # The smallest/largest possible values, as appropriate, so the map will display
        # something if there is no data
        north = [-80]
        west = [180]
        south = [80]
        east = [-180]

        for box in bounds.values():
            west.append(box[0])
            south.append(box[1])
            east.append(box[2])
            north.append(box[3])

        # The largest box that contains all the bounding boxes, how Leaflet wants it.
        return [[min(south), min(west)], [max(north), max(east)]]


    class Meta:
        verbose_name = "Location Information"

class SupplyKit(SingletonModel):
    """ A singleton model representing the supply kit information """
    days = models.PositiveIntegerField(
        default=3,
        help_text="The number of days' worth of supplies prepared residents should have on hand."
    )
    text = models.TextField(
        help_text="More information about building your supply kit. Any web address in here gets turned into a link automatically."
    )

class ImportantLink(models.Model):
    """ A model representing a link with a title """
    title = models.CharField(
        max_length=50,
        help_text="A title for your important link, like 'Evacuation Information'"
    )
    link = models.TextField(
        help_text="Your link and any information about it. Any web address in here gets turned into a link automatically."
    )
    def __str__(self):
        return self.title +': ' + self.link

class ShapeManager(models.GeoManager):
    def has_point(self, pnt):
        return self.filter(geom__contains=pnt)

    def data_bounds(self):
        return self.aggregate(Extent('geom'))['geom__extent']

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsClasses
class EQ_Fault_Buffer(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class EQ_Historic_Distance(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class EQ_Most_Like(models.Model):
    lookup_val = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class EQ_Worst_Case(models.Model):
    lookup_val = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class Fire_Hist_Bound(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class Fire_Intensity(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class Fire_Worst_Case_placeholder(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class Flood_Channel_Migration_Zones(models.Model):
    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class Flood_FEMA_DFRIM_2015(models.Model):
    femades = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.femades)

class Flood_Worst_Case_ph(models.Model):
    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

class Landslide_placeholder(models.Model):
    lookup_val = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    def __str__(self):
        return str(self.lookup_val)

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
    EQ_Historic_Distance_filter = models.ForeignKey(EQ_Historic_Distance, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    EQ_Most_Like_filter = models.ForeignKey(EQ_Most_Like, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    EQ_Worst_Case_filter = models.ForeignKey(EQ_Worst_Case, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Fire_Hist_Bound_filter = models.ForeignKey(Fire_Hist_Bound, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Fire_Intensity_filter = models.ForeignKey(Fire_Intensity, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Fire_Worst_Case_placeholder_filter = models.ForeignKey(Fire_Worst_Case_placeholder, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Flood_Channel_Migration_Zones_filter = models.ForeignKey(Flood_Channel_Migration_Zones, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Flood_FEMA_DFRIM_2015_filter = models.ForeignKey(Flood_FEMA_DFRIM_2015, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Flood_Worst_Case_ph_filter = models.ForeignKey(Flood_Worst_Case_ph, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    Landslide_placeholder_filter = models.ForeignKey(Landslide_placeholder, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
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
        EQ_Fault_Buffer_rating = qs_EQ_Fault_Buffer.values_list('lookup_val', flat=True)
        EQ_Fault_Buffer_snuggets = []
        for rating in EQ_Fault_Buffer_rating:
            individualSnugget = Snugget.objects.filter(EQ_Fault_Buffer_filter__lookup_val__exact=rating).select_subclasses()
            EQ_Fault_Buffer_snuggets.extend(individualSnugget)

        qs_EQ_Historic_Distance = EQ_Historic_Distance.objects.filter(geom__contains=pnt)
        EQ_Historic_Distance_rating = qs_EQ_Historic_Distance.values_list('lookup_val', flat=True)
        EQ_Historic_Distance_snuggets = []
        for rating in EQ_Historic_Distance_rating:
            individualSnugget = Snugget.objects.filter(EQ_Historic_Distance_filter__lookup_val__exact=rating).select_subclasses()
            EQ_Historic_Distance_snuggets.extend(individualSnugget)

        qs_EQ_Most_Like = EQ_Most_Like.objects.filter(geom__contains=pnt)
        EQ_Most_Like_rating = qs_EQ_Most_Like.values_list('lookup_val', flat=True)
        EQ_Most_Like_snuggets = []
        for rating in EQ_Most_Like_rating:
            individualSnugget = Snugget.objects.filter(EQ_Most_Like_filter__lookup_val__exact=rating).select_subclasses()
            EQ_Most_Like_snuggets.extend(individualSnugget)

        qs_EQ_Worst_Case = EQ_Worst_Case.objects.filter(geom__contains=pnt)
        EQ_Worst_Case_rating = qs_EQ_Worst_Case.values_list('lookup_val', flat=True)
        EQ_Worst_Case_snuggets = []
        for rating in EQ_Worst_Case_rating:
            individualSnugget = Snugget.objects.filter(EQ_Worst_Case_filter__lookup_val__exact=rating).select_subclasses()
            EQ_Worst_Case_snuggets.extend(individualSnugget)

        qs_Fire_Hist_Bound = Fire_Hist_Bound.objects.filter(geom__contains=pnt)
        Fire_Hist_Bound_rating = qs_Fire_Hist_Bound.values_list('lookup_val', flat=True)
        Fire_Hist_Bound_snuggets = []
        for rating in Fire_Hist_Bound_rating:
            individualSnugget = Snugget.objects.filter(Fire_Hist_Bound_filter__lookup_val__exact=rating).select_subclasses()
            Fire_Hist_Bound_snuggets.extend(individualSnugget)

        qs_Fire_Intensity = Fire_Intensity.objects.filter(geom__contains=pnt)
        Fire_Intensity_rating = qs_Fire_Intensity.values_list('lookup_val', flat=True)
        Fire_Intensity_snuggets = []
        for rating in Fire_Intensity_rating:
            individualSnugget = Snugget.objects.filter(Fire_Intensity_filter__lookup_val__exact=rating).select_subclasses()
            Fire_Intensity_snuggets.extend(individualSnugget)

        qs_Fire_Worst_Case_placeholder = Fire_Worst_Case_placeholder.objects.filter(geom__contains=pnt)
        Fire_Worst_Case_placeholder_rating = qs_Fire_Worst_Case_placeholder.values_list('lookup_val', flat=True)
        Fire_Worst_Case_placeholder_snuggets = []
        for rating in Fire_Worst_Case_placeholder_rating:
            individualSnugget = Snugget.objects.filter(Fire_Worst_Case_placeholder_filter__lookup_val__exact=rating).select_subclasses()
            Fire_Worst_Case_placeholder_snuggets.extend(individualSnugget)

        qs_Flood_Channel_Migration_Zones = Flood_Channel_Migration_Zones.objects.filter(geom__contains=pnt)
        Flood_Channel_Migration_Zones_rating = qs_Flood_Channel_Migration_Zones.values_list('lookup_val', flat=True)
        Flood_Channel_Migration_Zones_snuggets = []
        for rating in Flood_Channel_Migration_Zones_rating:
            individualSnugget = Snugget.objects.filter(Flood_Channel_Migration_Zones_filter__lookup_val__exact=rating).select_subclasses()
            Flood_Channel_Migration_Zones_snuggets.extend(individualSnugget)

        qs_Flood_FEMA_DFRIM_2015 = Flood_FEMA_DFRIM_2015.objects.filter(geom__contains=pnt)
        Flood_FEMA_DFRIM_2015_rating = qs_Flood_FEMA_DFRIM_2015.values_list('femades', flat=True)
        Flood_FEMA_DFRIM_2015_snuggets = []
        for rating in Flood_FEMA_DFRIM_2015_rating:
            individualSnugget = Snugget.objects.filter(Flood_FEMA_DFRIM_2015_filter__femades__exact=rating).select_subclasses()
            Flood_FEMA_DFRIM_2015_snuggets.extend(individualSnugget)

        qs_Flood_Worst_Case_ph = Flood_Worst_Case_ph.objects.filter(geom__contains=pnt)
        Flood_Worst_Case_ph_rating = qs_Flood_Worst_Case_ph.values_list('lookup_val', flat=True)
        Flood_Worst_Case_ph_snuggets = []
        for rating in Flood_Worst_Case_ph_rating:
            individualSnugget = Snugget.objects.filter(Flood_Worst_Case_ph_filter__lookup_val__exact=rating).select_subclasses()
            Flood_Worst_Case_ph_snuggets.extend(individualSnugget)

        qs_Landslide_placeholder = Landslide_placeholder.objects.filter(geom__contains=pnt)
        Landslide_placeholder_rating = qs_Landslide_placeholder.values_list('lookup_val', flat=True)
        Landslide_placeholder_snuggets = []
        for rating in Landslide_placeholder_rating:
            individualSnugget = Snugget.objects.filter(Landslide_placeholder_filter__lookup_val__exact=rating).select_subclasses()
            Landslide_placeholder_snuggets.extend(individualSnugget)


        return {'groups': {
                          'EQ_Fault_Buffer_snugs': EQ_Fault_Buffer_snuggets,
                          'EQ_Historic_Distance_snugs': EQ_Historic_Distance_snuggets,
                          'EQ_Most_Like_snugs': EQ_Most_Like_snuggets,
                          'EQ_Worst_Case_snugs': EQ_Worst_Case_snuggets,
                          'Fire_Hist_Bound_snugs': Fire_Hist_Bound_snuggets,
                          'Fire_Intensity_snugs': Fire_Intensity_snuggets,
                          'Fire_Worst_Case_placeholder_snugs': Fire_Worst_Case_placeholder_snuggets,
                          'Flood_Channel_Migration_Zones_snugs': Flood_Channel_Migration_Zones_snuggets,
                          'Flood_FEMA_DFRIM_2015_snugs': Flood_FEMA_DFRIM_2015_snuggets,
                          'Flood_Worst_Case_ph_snugs': Flood_Worst_Case_ph_snuggets,
                          'Landslide_placeholder_snugs': Landslide_placeholder_snuggets
                          },
                'EQ_Fault_Buffer_rating': EQ_Fault_Buffer_rating,
                'EQ_Historic_Distance_rating': EQ_Historic_Distance_rating,
                'EQ_Most_Like_rating': EQ_Most_Like_rating,
                'EQ_Worst_Case_rating': EQ_Worst_Case_rating,
                'Fire_Hist_Bound_rating': Fire_Hist_Bound_rating,
                'Fire_Intensity_rating': Fire_Intensity_rating,
                'Fire_Worst_Case_placeholder_rating': Fire_Worst_Case_placeholder_rating,
                'Flood_Channel_Migration_Zones_rating': Flood_Channel_Migration_Zones_rating,
                'Flood_FEMA_DFRIM_2015_rating': Flood_FEMA_DFRIM_2015_rating,
                'Flood_Worst_Case_ph_rating': Flood_Worst_Case_ph_rating,
                'Landslide_placeholder_rating': Landslide_placeholder_rating
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
