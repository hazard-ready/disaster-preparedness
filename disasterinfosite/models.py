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
from django.contrib.postgres.validators import RangeMinValueValidator, RangeMaxValueValidator


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
    area_name = models.CharField(
        max_length=100,
        default="the affected area",
        help_text="Describe the entire area that this app covers, e.g. 'Oregon' or 'Missoula County'."
    )
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

    def __unicode__(self):
        return u"Location Information"

    @staticmethod
    def get_data_bounds():
        bounds = {
    ######################################################
    # GENERATED CODE GOES HERE
    # DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
    # locationsList
            'RDPO_region_quake': RDPO_region_quake.objects.data_bounds(),
            'RDPO_region_winter': RDPO_region_winter.objects.data_bounds(),
            'RDPO_Lsd_Clark': RDPO_Lsd_Clark.objects.data_bounds(),
            'RDPO_counties_quake': RDPO_counties_quake.objects.data_bounds(),
            'RDPOflood_OR': RDPOflood_OR.objects.data_bounds(),
            'RDPO_counties_volcano': RDPO_counties_volcano.objects.data_bounds(),
            'RDPO_Lsld_OR': RDPO_Lsld_OR.objects.data_bounds(),
            'RDPOFire_Clark': RDPOFire_Clark.objects.data_bounds(),
            'RDPO_region_summer': RDPO_region_summer.objects.data_bounds(),
            'RDPO_region_fire': RDPO_region_fire.objects.data_bounds(),
            'RDPOCascadiaM9_3_Clark': RDPOCascadiaM9_3_Clark.objects.data_bounds(),
            'RDPOFire_OR': RDPOFire_OR.objects.data_bounds(),
            'RDPO_region_volcano': RDPO_region_volcano.objects.data_bounds(),
            'RDPOLiquefaction_OR': RDPOLiquefaction_OR.objects.data_bounds(),
            'RDPOCascadiaM9_Col': RDPOCascadiaM9_Col.objects.data_bounds(),
            'RDPOflood_clark': RDPOflood_clark.objects.data_bounds(),
            'RDPO_region_flood': RDPO_region_flood.objects.data_bounds(),
            'RDPOvolcanoes': RDPOvolcanoes.objects.data_bounds(),
            'RDPO_counties_winter': RDPO_counties_winter.objects.data_bounds(),
            'RDPO_counties_fire': RDPO_counties_fire.objects.data_bounds(),
            'RDPO_WA': RDPO_WA.objects.data_bounds(),
            'RDPO_counties_flood': RDPO_counties_flood.objects.data_bounds(),
            'RDPO_OR': RDPO_OR.objects.data_bounds(),
            'RDPOCascadiaM9_3Cnty': RDPOCascadiaM9_3Cnty.objects.data_bounds(),
            'RDPO_region_slide': RDPO_region_slide.objects.data_bounds(),
            'RDPOCascadiaM9_OR': RDPOCascadiaM9_OR.objects.data_bounds(),
            'RDPOLiquefact_Clark': RDPOLiquefact_Clark.objects.data_bounds(),
            'RDPO_counties_summer': RDPO_counties_summer.objects.data_bounds(),
            'RDPOhistflood': RDPOhistflood.objects.data_bounds(),
            'RDPO_counties_slide': RDPO_counties_slide.objects.data_bounds()
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
    note = models.TextField(blank=True, help_text='A note that appears above all snuggets in this section. Use for data caveats or warnings.')

    def __str__(self):
        return self.name

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# modelsClasses
class RDPO_region_quake(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_region_winter(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='winter')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_Lsd_Clark(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='slide')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_counties_quake(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOflood_OR(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='flood')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_counties_volcano(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='volcano')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_Lsld_OR(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='slide')[0]

    rast = models.RasterField(srid=4326)
    bbox = models.PolygonField(srid=4326)
    objects = RasterManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.rast.name) + ',	' + str(self.bbox)

class RDPOFire_Clark(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='fire')[0]

    rast = models.RasterField(srid=4326)
    bbox = models.PolygonField(srid=4326)
    objects = RasterManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.rast.name) + ',	' + str(self.bbox)

class RDPO_region_summer(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='summer')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_region_fire(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='fire')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOCascadiaM9_3_Clark(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOFire_OR(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='fire')[0]

    rast = models.RasterField(srid=4326)
    bbox = models.PolygonField(srid=4326)
    objects = RasterManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.rast.name) + ',	' + str(self.bbox)

class RDPO_region_volcano(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='volcano')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOLiquefaction_OR(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOCascadiaM9_Col(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    rast = models.RasterField(srid=4326)
    bbox = models.PolygonField(srid=4326)
    objects = RasterManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.rast.name) + ',	' + str(self.bbox)

class RDPOflood_clark(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='flood')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_region_flood(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='flood')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOvolcanoes(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='volcano')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_counties_winter(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='winter')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_counties_fire(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='fire')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_WA(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='slide')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_counties_flood(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='flood')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_OR(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='slide')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOCascadiaM9_3Cnty(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    rast = models.RasterField(srid=4326)
    bbox = models.PolygonField(srid=4326)
    objects = RasterManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.rast.name) + ',	' + str(self.bbox)

class RDPO_region_slide(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='slide')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOCascadiaM9_OR(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    lookup_val = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOLiquefact_Clark(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='quake')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_counties_summer(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='summer')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPOhistflood(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='flood')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

class RDPO_counties_slide(models.Model):
    def getGroup():
        return ShapefileGroup.objects.get_or_create(name='slide')[0]

    lookup_val = models.CharField(max_length=80)
    geom = models.MultiPolygonField(srid=4326)
    objects = ShapeManager()

    group = models.ForeignKey(ShapefileGroup, default=getGroup, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.lookup_val)

# END OF GENERATED CODE BLOCK
######################################################

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
    RDPO_region_quake_filter = models.ForeignKey(RDPO_region_quake, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_region_winter_filter = models.ForeignKey(RDPO_region_winter, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_Lsd_Clark_filter = models.ForeignKey(RDPO_Lsd_Clark, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_counties_quake_filter = models.ForeignKey(RDPO_counties_quake, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOflood_OR_filter = models.ForeignKey(RDPOflood_OR, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_counties_volcano_filter = models.ForeignKey(RDPO_counties_volcano, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_Lsld_OR_filter = models.IntegerField(null=True)
    RDPOFire_Clark_filter = models.IntegerField(null=True)
    RDPO_region_summer_filter = models.ForeignKey(RDPO_region_summer, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_region_fire_filter = models.ForeignKey(RDPO_region_fire, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOCascadiaM9_3_Clark_filter = models.ForeignKey(RDPOCascadiaM9_3_Clark, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOFire_OR_filter = models.IntegerField(null=True)
    RDPO_region_volcano_filter = models.ForeignKey(RDPO_region_volcano, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOLiquefaction_OR_filter = models.ForeignKey(RDPOLiquefaction_OR, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOCascadiaM9_Col_filter = models.IntegerField(null=True)
    RDPOflood_clark_filter = models.ForeignKey(RDPOflood_clark, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_region_flood_filter = models.ForeignKey(RDPO_region_flood, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOvolcanoes_filter = models.ForeignKey(RDPOvolcanoes, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_counties_winter_filter = models.ForeignKey(RDPO_counties_winter, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_counties_fire_filter = models.ForeignKey(RDPO_counties_fire, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_WA_filter = models.ForeignKey(RDPO_WA, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_counties_flood_filter = models.ForeignKey(RDPO_counties_flood, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_OR_filter = models.ForeignKey(RDPO_OR, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOCascadiaM9_3Cnty_filter = models.IntegerField(null=True)
    RDPO_region_slide_filter = models.ForeignKey(RDPO_region_slide, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOCascadiaM9_OR_filter = models.ForeignKey(RDPOCascadiaM9_OR, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOLiquefact_Clark_filter = models.ForeignKey(RDPOLiquefact_Clark, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_counties_summer_filter = models.ForeignKey(RDPO_counties_summer, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPOhistflood_filter = models.ForeignKey(RDPOhistflood, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    RDPO_counties_slide_filter = models.ForeignKey(RDPO_counties_slide, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
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
        qs_RDPO_region_quake = RDPO_region_quake.objects.filter(geom__contains=pnt)
        RDPO_region_quake_rating = qs_RDPO_region_quake.values_list('lookup_val', flat=True)
        for rating in RDPO_region_quake_rating:
            RDPO_region_quake_snugget = Snugget.objects.filter(RDPO_region_quake_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_region_quake_snugget:
                groupsDict[RDPO_region_quake.getGroup()].extend(RDPO_region_quake_snugget)

        qs_RDPO_region_winter = RDPO_region_winter.objects.filter(geom__contains=pnt)
        RDPO_region_winter_rating = qs_RDPO_region_winter.values_list('lookup_val', flat=True)
        for rating in RDPO_region_winter_rating:
            RDPO_region_winter_snugget = Snugget.objects.filter(RDPO_region_winter_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_region_winter_snugget:
                groupsDict[RDPO_region_winter.getGroup()].extend(RDPO_region_winter_snugget)

        qs_RDPO_Lsd_Clark = RDPO_Lsd_Clark.objects.filter(geom__contains=pnt)
        RDPO_Lsd_Clark_rating = qs_RDPO_Lsd_Clark.values_list('lookup_val', flat=True)
        for rating in RDPO_Lsd_Clark_rating:
            RDPO_Lsd_Clark_snugget = Snugget.objects.filter(RDPO_Lsd_Clark_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_Lsd_Clark_snugget:
                groupsDict[RDPO_Lsd_Clark.getGroup()].extend(RDPO_Lsd_Clark_snugget)

        qs_RDPO_counties_quake = RDPO_counties_quake.objects.filter(geom__contains=pnt)
        RDPO_counties_quake_rating = qs_RDPO_counties_quake.values_list('lookup_val', flat=True)
        for rating in RDPO_counties_quake_rating:
            RDPO_counties_quake_snugget = Snugget.objects.filter(RDPO_counties_quake_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_counties_quake_snugget:
                groupsDict[RDPO_counties_quake.getGroup()].extend(RDPO_counties_quake_snugget)

        qs_RDPOflood_OR = RDPOflood_OR.objects.filter(geom__contains=pnt)
        RDPOflood_OR_rating = qs_RDPOflood_OR.values_list('lookup_val', flat=True)
        for rating in RDPOflood_OR_rating:
            RDPOflood_OR_snugget = Snugget.objects.filter(RDPOflood_OR_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOflood_OR_snugget:
                groupsDict[RDPOflood_OR.getGroup()].extend(RDPOflood_OR_snugget)

        qs_RDPO_counties_volcano = RDPO_counties_volcano.objects.filter(geom__contains=pnt)
        RDPO_counties_volcano_rating = qs_RDPO_counties_volcano.values_list('lookup_val', flat=True)
        for rating in RDPO_counties_volcano_rating:
            RDPO_counties_volcano_snugget = Snugget.objects.filter(RDPO_counties_volcano_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_counties_volcano_snugget:
                groupsDict[RDPO_counties_volcano.getGroup()].extend(RDPO_counties_volcano_snugget)

        RDPO_Lsld_OR_rating = rasterPointLookup(RDPO_Lsld_OR, lng, lat)
        if RDPO_Lsld_OR_rating is not None:
            RDPO_Lsld_OR_snugget = Snugget.objects.filter(RDPO_Lsld_OR_filter__exact=RDPO_Lsld_OR_rating).order_by('order').select_subclasses()
            if RDPO_Lsld_OR_snugget:
                groupsDict[RDPO_Lsld_OR.getGroup()].extend(RDPO_Lsld_OR_snugget)

        RDPOFire_Clark_rating = rasterPointLookup(RDPOFire_Clark, lng, lat)
        if RDPOFire_Clark_rating is not None:
            RDPOFire_Clark_snugget = Snugget.objects.filter(RDPOFire_Clark_filter__exact=RDPOFire_Clark_rating).order_by('order').select_subclasses()
            if RDPOFire_Clark_snugget:
                groupsDict[RDPOFire_Clark.getGroup()].extend(RDPOFire_Clark_snugget)

        qs_RDPO_region_summer = RDPO_region_summer.objects.filter(geom__contains=pnt)
        RDPO_region_summer_rating = qs_RDPO_region_summer.values_list('lookup_val', flat=True)
        for rating in RDPO_region_summer_rating:
            RDPO_region_summer_snugget = Snugget.objects.filter(RDPO_region_summer_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_region_summer_snugget:
                groupsDict[RDPO_region_summer.getGroup()].extend(RDPO_region_summer_snugget)

        qs_RDPO_region_fire = RDPO_region_fire.objects.filter(geom__contains=pnt)
        RDPO_region_fire_rating = qs_RDPO_region_fire.values_list('lookup_val', flat=True)
        for rating in RDPO_region_fire_rating:
            RDPO_region_fire_snugget = Snugget.objects.filter(RDPO_region_fire_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_region_fire_snugget:
                groupsDict[RDPO_region_fire.getGroup()].extend(RDPO_region_fire_snugget)

        qs_RDPOCascadiaM9_3_Clark = RDPOCascadiaM9_3_Clark.objects.filter(geom__contains=pnt)
        RDPOCascadiaM9_3_Clark_rating = qs_RDPOCascadiaM9_3_Clark.values_list('lookup_val', flat=True)
        for rating in RDPOCascadiaM9_3_Clark_rating:
            RDPOCascadiaM9_3_Clark_snugget = Snugget.objects.filter(RDPOCascadiaM9_3_Clark_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOCascadiaM9_3_Clark_snugget:
                groupsDict[RDPOCascadiaM9_3_Clark.getGroup()].extend(RDPOCascadiaM9_3_Clark_snugget)

        RDPOFire_OR_rating = rasterPointLookup(RDPOFire_OR, lng, lat)
        if RDPOFire_OR_rating is not None:
            RDPOFire_OR_snugget = Snugget.objects.filter(RDPOFire_OR_filter__exact=RDPOFire_OR_rating).order_by('order').select_subclasses()
            if RDPOFire_OR_snugget:
                groupsDict[RDPOFire_OR.getGroup()].extend(RDPOFire_OR_snugget)

        qs_RDPO_region_volcano = RDPO_region_volcano.objects.filter(geom__contains=pnt)
        RDPO_region_volcano_rating = qs_RDPO_region_volcano.values_list('lookup_val', flat=True)
        for rating in RDPO_region_volcano_rating:
            RDPO_region_volcano_snugget = Snugget.objects.filter(RDPO_region_volcano_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_region_volcano_snugget:
                groupsDict[RDPO_region_volcano.getGroup()].extend(RDPO_region_volcano_snugget)

        qs_RDPOLiquefaction_OR = RDPOLiquefaction_OR.objects.filter(geom__contains=pnt)
        RDPOLiquefaction_OR_rating = qs_RDPOLiquefaction_OR.values_list('lookup_val', flat=True)
        for rating in RDPOLiquefaction_OR_rating:
            RDPOLiquefaction_OR_snugget = Snugget.objects.filter(RDPOLiquefaction_OR_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOLiquefaction_OR_snugget:
                groupsDict[RDPOLiquefaction_OR.getGroup()].extend(RDPOLiquefaction_OR_snugget)

        RDPOCascadiaM9_Col_rating = rasterPointLookup(RDPOCascadiaM9_Col, lng, lat)
        if RDPOCascadiaM9_Col_rating is not None:
            RDPOCascadiaM9_Col_snugget = Snugget.objects.filter(RDPOCascadiaM9_Col_filter__exact=RDPOCascadiaM9_Col_rating).order_by('order').select_subclasses()
            if RDPOCascadiaM9_Col_snugget:
                groupsDict[RDPOCascadiaM9_Col.getGroup()].extend(RDPOCascadiaM9_Col_snugget)

        qs_RDPOflood_clark = RDPOflood_clark.objects.filter(geom__contains=pnt)
        RDPOflood_clark_rating = qs_RDPOflood_clark.values_list('lookup_val', flat=True)
        for rating in RDPOflood_clark_rating:
            RDPOflood_clark_snugget = Snugget.objects.filter(RDPOflood_clark_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOflood_clark_snugget:
                groupsDict[RDPOflood_clark.getGroup()].extend(RDPOflood_clark_snugget)

        qs_RDPO_region_flood = RDPO_region_flood.objects.filter(geom__contains=pnt)
        RDPO_region_flood_rating = qs_RDPO_region_flood.values_list('lookup_val', flat=True)
        for rating in RDPO_region_flood_rating:
            RDPO_region_flood_snugget = Snugget.objects.filter(RDPO_region_flood_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_region_flood_snugget:
                groupsDict[RDPO_region_flood.getGroup()].extend(RDPO_region_flood_snugget)

        qs_RDPOvolcanoes = RDPOvolcanoes.objects.filter(geom__contains=pnt)
        RDPOvolcanoes_rating = qs_RDPOvolcanoes.values_list('lookup_val', flat=True)
        for rating in RDPOvolcanoes_rating:
            RDPOvolcanoes_snugget = Snugget.objects.filter(RDPOvolcanoes_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOvolcanoes_snugget:
                groupsDict[RDPOvolcanoes.getGroup()].extend(RDPOvolcanoes_snugget)

        qs_RDPO_counties_winter = RDPO_counties_winter.objects.filter(geom__contains=pnt)
        RDPO_counties_winter_rating = qs_RDPO_counties_winter.values_list('lookup_val', flat=True)
        for rating in RDPO_counties_winter_rating:
            RDPO_counties_winter_snugget = Snugget.objects.filter(RDPO_counties_winter_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_counties_winter_snugget:
                groupsDict[RDPO_counties_winter.getGroup()].extend(RDPO_counties_winter_snugget)

        qs_RDPO_counties_fire = RDPO_counties_fire.objects.filter(geom__contains=pnt)
        RDPO_counties_fire_rating = qs_RDPO_counties_fire.values_list('lookup_val', flat=True)
        for rating in RDPO_counties_fire_rating:
            RDPO_counties_fire_snugget = Snugget.objects.filter(RDPO_counties_fire_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_counties_fire_snugget:
                groupsDict[RDPO_counties_fire.getGroup()].extend(RDPO_counties_fire_snugget)

        qs_RDPO_WA = RDPO_WA.objects.filter(geom__contains=pnt)
        RDPO_WA_rating = qs_RDPO_WA.values_list('lookup_val', flat=True)
        for rating in RDPO_WA_rating:
            RDPO_WA_snugget = Snugget.objects.filter(RDPO_WA_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_WA_snugget:
                groupsDict[RDPO_WA.getGroup()].extend(RDPO_WA_snugget)

        qs_RDPO_counties_flood = RDPO_counties_flood.objects.filter(geom__contains=pnt)
        RDPO_counties_flood_rating = qs_RDPO_counties_flood.values_list('lookup_val', flat=True)
        for rating in RDPO_counties_flood_rating:
            RDPO_counties_flood_snugget = Snugget.objects.filter(RDPO_counties_flood_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_counties_flood_snugget:
                groupsDict[RDPO_counties_flood.getGroup()].extend(RDPO_counties_flood_snugget)

        qs_RDPO_OR = RDPO_OR.objects.filter(geom__contains=pnt)
        RDPO_OR_rating = qs_RDPO_OR.values_list('lookup_val', flat=True)
        for rating in RDPO_OR_rating:
            RDPO_OR_snugget = Snugget.objects.filter(RDPO_OR_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_OR_snugget:
                groupsDict[RDPO_OR.getGroup()].extend(RDPO_OR_snugget)

        RDPOCascadiaM9_3Cnty_rating = rasterPointLookup(RDPOCascadiaM9_3Cnty, lng, lat)
        if RDPOCascadiaM9_3Cnty_rating is not None:
            RDPOCascadiaM9_3Cnty_snugget = Snugget.objects.filter(RDPOCascadiaM9_3Cnty_filter__exact=RDPOCascadiaM9_3Cnty_rating).order_by('order').select_subclasses()
            if RDPOCascadiaM9_3Cnty_snugget:
                groupsDict[RDPOCascadiaM9_3Cnty.getGroup()].extend(RDPOCascadiaM9_3Cnty_snugget)

        qs_RDPO_region_slide = RDPO_region_slide.objects.filter(geom__contains=pnt)
        RDPO_region_slide_rating = qs_RDPO_region_slide.values_list('lookup_val', flat=True)
        for rating in RDPO_region_slide_rating:
            RDPO_region_slide_snugget = Snugget.objects.filter(RDPO_region_slide_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_region_slide_snugget:
                groupsDict[RDPO_region_slide.getGroup()].extend(RDPO_region_slide_snugget)

        qs_RDPOCascadiaM9_OR = RDPOCascadiaM9_OR.objects.filter(geom__contains=pnt)
        RDPOCascadiaM9_OR_rating = qs_RDPOCascadiaM9_OR.values_list('lookup_val', flat=True)
        for rating in RDPOCascadiaM9_OR_rating:
            RDPOCascadiaM9_OR_snugget = Snugget.objects.filter(RDPOCascadiaM9_OR_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOCascadiaM9_OR_snugget:
                groupsDict[RDPOCascadiaM9_OR.getGroup()].extend(RDPOCascadiaM9_OR_snugget)

        qs_RDPOLiquefact_Clark = RDPOLiquefact_Clark.objects.filter(geom__contains=pnt)
        RDPOLiquefact_Clark_rating = qs_RDPOLiquefact_Clark.values_list('lookup_val', flat=True)
        for rating in RDPOLiquefact_Clark_rating:
            RDPOLiquefact_Clark_snugget = Snugget.objects.filter(RDPOLiquefact_Clark_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOLiquefact_Clark_snugget:
                groupsDict[RDPOLiquefact_Clark.getGroup()].extend(RDPOLiquefact_Clark_snugget)

        qs_RDPO_counties_summer = RDPO_counties_summer.objects.filter(geom__contains=pnt)
        RDPO_counties_summer_rating = qs_RDPO_counties_summer.values_list('lookup_val', flat=True)
        for rating in RDPO_counties_summer_rating:
            RDPO_counties_summer_snugget = Snugget.objects.filter(RDPO_counties_summer_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_counties_summer_snugget:
                groupsDict[RDPO_counties_summer.getGroup()].extend(RDPO_counties_summer_snugget)

        qs_RDPOhistflood = RDPOhistflood.objects.filter(geom__contains=pnt)
        RDPOhistflood_rating = qs_RDPOhistflood.values_list('lookup_val', flat=True)
        for rating in RDPOhistflood_rating:
            RDPOhistflood_snugget = Snugget.objects.filter(RDPOhistflood_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPOhistflood_snugget:
                groupsDict[RDPOhistflood.getGroup()].extend(RDPOhistflood_snugget)

        qs_RDPO_counties_slide = RDPO_counties_slide.objects.filter(geom__contains=pnt)
        RDPO_counties_slide_rating = qs_RDPO_counties_slide.values_list('lookup_val', flat=True)
        for rating in RDPO_counties_slide_rating:
            RDPO_counties_slide_snugget = Snugget.objects.filter(RDPO_counties_slide_filter__lookup_val__exact=rating).order_by('order').select_subclasses()
            if RDPO_counties_slide_snugget:
                groupsDict[RDPO_counties_slide.getGroup()].extend(RDPO_counties_slide_snugget)

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

class PreparednessAction(models.Model):
    title = models.TextField(default="")
    image = models.ImageField(upload_to="prepare_images")
    cost = models.IntegerField(default=0,
        validators=[
            RangeMinValueValidator(0),
            RangeMaxValueValidator(4)
        ])
    happy_text = models.TextField(default="")
    useful_text = models.TextField(default="")
    property_text = models.TextField(default="")
    content_text = models.TextField(default="")
    link_text = models.TextField(default="")
    link_icon = models.ImageField(upload_to="prepare_images")
    link = models.URLField(default="")
    slug = models.TextField(default="")


class SurveyCode(models.Model):
    code = models.TextField(default="")

    def __str__(self):
        return self.code
