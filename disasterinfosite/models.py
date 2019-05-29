from collections import OrderedDict
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.gdal import OGRGeometry
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import Extent
from embed_video.fields import EmbedVideoField
from model_utils.managers import InheritanceManager
from solo.models import SingletonModel
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_save
from django.dispatch import receiver


SNUG_TEXT = 0
SNUG_VIDEO = 1
SNUG_SLIDESHOW = 2

SNUGGET_TYPES = (
                 ('SNUG_TEXT', 'TextSnugget'),
                 ('SNUG_VIDEO', 'EmbedSnugget'),
                 ('SNUG_SLIDESHOW', 'SlideshowSnugget')
                )

class UserProfile(models.Model):
    """ A model representing a user's information that isn't their username, password, or email address """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "User Profile"

    def __str__(self):
        return "{0}: {1}, {2} {3}, {4} {5}".format(self.user, self.address1, self.address2, self.city, self.state, self.zip_code)


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
        default="https://www.example.com",
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
            if box is not None:
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

    @property
    def meals(self):
        return 3 * self.days

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

class ShapeManager(models.Manager):
    def data_bounds(self):
        return self.aggregate(Extent('geom'))['geom__extent']


class RasterManager(models.Manager):
    def data_bounds(self):
        return self.aggregate(Extent('bbox'))['bbox__extent']




class ShapefileGroup(models.Model):
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50, default="")
    order_of_appearance = models.IntegerField(
        default=0,
        help_text="The order, from top to bottom, in which you would like this group to appear, when applicable."
    )
    likely_scenario_title = models.CharField(max_length=80, blank=True)
    likely_scenario_text = models.TextField(blank=True)

    def __str__(self):
        return self.name

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsClasses
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
    display_name = models.CharField(max_length=50, help_text="The name to show for this section", default="")
    collapsible = models.BooleanField(default=True, help_text='Whether this section of the data is collapsible')
    order_of_appearance = models.IntegerField(
        default=0,
        help_text="The order in which you'd like this to appear in the tab. 0 is at the top."
    )

    def __str__(self):
        return self.name

class SnuggetPopOut(models.Model):
    text = models.TextField(default='')
    image = models.ImageField(upload_to="popout_images")
    link = models.TextField(default='', max_length=255)
    alt_text = models.TextField(default='', max_length=255)
    video = EmbedVideoField(null=True)

    @property
    def has_content(self):
        "Returns true if this popout has some content"
        return (self.text or self.image or self.link or self.video)

    def __str__(self):
        return self.text[:100]


@receiver(pre_save, sender=SnuggetSection)
@receiver(pre_save, sender=ShapefileGroup)
def default_display_name(sender, instance, *args, **kwargs):
    if not instance.display_name:
        instance.display_name = instance.name


# looks up a point in a set of rasters and returns the first non-NODATA value it finds
# or None if there are no rasters, the point is not within any of them or it's in a NODATA pixel.
# raster algebra taken from the django-raster project version 0.6 at
# https://github.com/geodesign/django-raster/blob/master/raster/utils.py
def rasterPointLookup(rasterCollection, lng, lat, band=0):
    # if we have no data at all, then save time and return None immediately
    sampleBBOX = rasterCollection.objects.only("bbox").first().bbox
    if sampleBBOX is None:
        return None

    rasterPoint = OGRGeometry('POINT({0} {1})'.format(lng, lat), srs=sampleBBOX.srs)
    vectorPoint = Point(lng, lat, srid=sampleBBOX.srid)

    # Using the filter here lets PostGIS do an indexed search on the bbox field, which is much faster than stepping through the objects.
    # Note that it will almost always only return one raster, but there could theoretically be 2 or 4 if our point is perfectly on a tile boundary.
    # In that instance, we return the first non-NODATA value we find.
    for tile in rasterCollection.objects.filter(bbox__contains=vectorPoint).all():
        # only bother to check for data if we're within the bounds
        rst = tile.rast
        offset = (abs(rst.origin.x - rasterPoint.coords[0]), abs(rst.origin.y - rasterPoint.coords[1]))
        offset_idx = [int(offset[0] / abs(rst.scale.x)), int(offset[1] / abs(rst.scale.y))]

        # points very close to the boundary can get rounded to 1 pixel beyond it, so fix that here
        if offset_idx[0] == rst.width:
            offset_idx[0] -= 1
        if offset_idx[1] == rst.height:
            offset_idx[1] -= 1

        result = rst.bands[band].data(offset=offset_idx, size=(1,1))[0]
        if result != rst.bands[band].nodata_value:
            return rst.bands[band].data(offset=offset_idx, size=(1,1))[0]

    return None





class Snugget(models.Model):
    objects = InheritanceManager()

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsFilters
# END OF GENERATED CODE BLOCK
######################################################

    section = models.ForeignKey(SnuggetSection, related_name='+', on_delete=models.PROTECT)
    group = models.ForeignKey(ShapefileGroup, on_delete=models.PROTECT, null=True)
    pop_out = models.OneToOneField(SnuggetPopOut, on_delete=models.PROTECT, blank=True, null=True)
    percentage = models.FloatField(null=True)
    order = models.IntegerField(default=0)

    def getRelatedTemplate(self):
        return "snugget.html"

    @staticmethod
    def findSnuggetsForPoint(lat=0, lng=0, merge_deform = True):
        pnt = Point(lng, lat)
        groups = ShapefileGroup.objects.all().order_by('order_of_appearance')
        groupsDict = OrderedDict({el:[] for el in groups})

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsGeoFilters
# END OF GENERATED CODE BLOCK
######################################################
        return groupsDict


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
    name = SNUGGET_TYPES[SNUG_VIDEO]
    text = models.TextField(default="")
    video = EmbedVideoField()

    def getRelatedTemplate(self):
        return "snugget_embed.html"

    def __str__(self):
        return "Embed Snugget: " + str(self.video)


class SlideshowSnugget(Snugget):
    name = SNUGGET_TYPES[SNUG_SLIDESHOW]
    text = models.TextField(default="")

    def getRelatedTemplate(self):
        return "snugget_slideshow.html"

    def __str__(self):
        return "Slideshow Snugget: " + str(self.text)


class PastEventsPhoto(models.Model):
    snugget = models.ForeignKey(SlideshowSnugget, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to="photos")
    caption = models.TextField(default="", max_length=200)

    def __str__(self):
        return str(self.image.url) + ' Caption: ' + str(self.caption)

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        self.delete(name)
        return name

class DataOverviewImage(models.Model):
    link_text = models.CharField(default="", max_length=100)
    image = models.ImageField(upload_to="data", storage=OverwriteStorage())

    def __str__(self):
        return self.image.url
