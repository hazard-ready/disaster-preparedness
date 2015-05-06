from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from embed_video.fields import EmbedVideoField
from model_utils.managers import InheritanceManager


zoneOptions = {
                1: 'Eastern',
                2: 'Valley',
                3: 'Coastal',
                4: 'Tsunami',
                }


SNUG_TEXT = 0
SNUG_AUDIO = 1
SNUG_VID = 2

SNUGGET_TYPES = (
                 ('SNUG_TEXT', 'TextSnugget'),
                 )


# This was originally an auto-generated Django model module created by ogrinspect,
# updated and documented by the devs.
class TsunamiZone(models.Model):
    type = models.CharField(max_length=50)
    typeid = models.IntegerField()
    geom = models.MultiPolygonField(srid=4326)  # This is for tsunamiZone
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.type


# This was an auto-generated Django model module created by ogrinspect with.
class ImpactZoneData(models.Model):
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    zoneid = models.IntegerField()
    zone = models.CharField(max_length=10)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return self.zone


# HAZARDS
# This is an auto-generated Django model module created by ogrinspect.
class ExpectedGroundShaking(models.Model):
    rate = models.IntegerField()
    shaking = models.CharField(max_length=11)
    geom = models.MultiPolygonField(srid=2992)  # This is for Groundshaking_Simple.
    objects = models.GeoManager()

    def __str__(self):
        return "Shaking: " + self.shaking + " (rate: " + str(self.rate) + ")"


class LandslideDeformation(models.Model):
    score = models.IntegerField()  # The number rating on the scale of ground deformation.
    label = models.CharField(max_length=11)  # The classification "Med, High, Low" etc.
    geom = models.MultiPolygonField(srid=2992)  # This is for Landlide_simple
    objects = models.GeoManager()

    def __str__(self):
        return "LandslideDeform: " + self.label


class LiquefactionDeformation(models.Model):
    score = models.IntegerField()  # The number rating on the scale of ground deformation
    label = models.CharField(max_length=11)  # The classification "Med, High, Low" etc.
    geom = models.MultiPolygonField(srid=2992)  # This is for Liquefaction_simple
    objects = models.GeoManager()

    def __str__(self):
        return "LiquefactionDeform: " + self.label


class ImpactZone(models.Model):
    name = models.CharField(max_length=50)
    featureValue = models.IntegerField()  # If/when ImpactZoneData gets cleaned up this could become a ForeignKey

    def __str__(self):
        return self.name


class RecoveryLevels(models.Model):
    name = models.CharField(max_length=50)
    shortLabel = models.CharField(max_length=2)
    description = models.TextField()

    def __str__(self):
        return self.name


class Infrastructure(models.Model):
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(ImpactZone, related_name='+', on_delete=models.PROTECT)
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
    zone = models.ForeignKey(ImpactZone, related_name='+', on_delete=models.PROTECT)
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
    shaking_filter = models.ForeignKey(ExpectedGroundShaking, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    impact_zone_filter = models.ForeignKey(ImpactZone, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    tsunami_filter = models.ForeignKey(TsunamiZone, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    liquifaction_filter = models.ForeignKey(LiquefactionDeformation, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    landslide_filter = models.ForeignKey(LandslideDeformation, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    temp_text_field = models.TextField(null=True, blank=True, editable=False)

    section = models.ForeignKey(SnuggetSection, related_name='+', on_delete=models.PROTECT)
    sub_section = models.ForeignKey(SnuggetSubSection, related_name='+', on_delete=models.PROTECT, null=True, blank=True)

    def getRelatedTemplate(self):
        return "snugget.html"

    @staticmethod
    def findSnuggetsForPoint(lat=0, lng=0, merge_deform = True):
        pnt = Point(lng, lat)
        qs_impacts = ImpactZoneData.objects.filter(geom__contains=pnt)
        print(qs_impacts)
        qs_tsunami = TsunamiZone.objects.filter(geom__contains=pnt)
        print(qs_tsunami)
        qs_shaking = ExpectedGroundShaking.objects.filter(geom__contains=pnt)
        print(qs_shaking)
        qs_liquifaction = LiquefactionDeformation.objects.filter(geom__contains=pnt)
        print(qs_liquifaction)
        qs_landslide = LandslideDeformation.objects.filter(geom__contains=pnt)
        print(qs_landslide)

        # bend, or
        # world.models.Snugget.findSnuggetsForPoint(lng=-121.3153096, lat=44.0581728)
        # Near seaside
        # world.models.Snugget.findSnuggetsForPoint(lng=-123.9125932, lat=45.9928274)
        
        liquifaction_scores = qs_liquifaction.values_list('score', flat=True)
        landslide_scores = qs_landslide.values_list('score', flat=True)
        shake_rating = qs_shaking.values_list('shaking', flat=True)        
        tsunami_snuggets = Snugget.objects.filter(tsunami_filter__typeid__in=qs_tsunami.values_list('typeid')).select_subclasses()
        shake_snuggets = Snugget.objects.filter(shaking_filter__shaking__in=shake_rating).select_subclasses()
        impact_snuggets = Snugget.objects.filter(impact_zone_filter__featureValue__in=qs_impacts.values_list('zoneid')).select_subclasses()
        liquifaction_snuggets = Snugget.objects.filter(liquifaction_filter__score__in=liquifaction_scores).select_subclasses()
        landslide_snuggets = Snugget.objects.filter(landslide_filter__score__in=landslide_scores).select_subclasses()
        
        deform_snuggets = []
        deform_rating = 0.0
        if (merge_deform == True):
            deform_snuggets = landslide_snuggets | liquifaction_snuggets
            both_scores = list(liquifaction_scores) + list(landslide_scores)
            if both_scores:
                deform_rating = max(both_scores)
        
        impact_zones = qs_impacts.values()

        return {'groups': {
                          'tsunami_snugs': tsunami_snuggets,
                          'shake_snugs': shake_snuggets,
                          'impact_snugs': impact_snuggets,
                          'liqui_snugs': liquifaction_snuggets,
                          'landslide_snugs': landslide_snuggets,
                          'deform_snugs': deform_snuggets,
                          },
                'deform_score': deform_rating,
                'shake_score': shake_rating,
                'impact_zones': impact_zones
                }

    def __str__(self):
        return "Basic Snugget.  If you see this string, you probably should file a bug report."


class TextSnugget(Snugget):
    name = SNUGGET_TYPES[SNUG_TEXT]
    content = models.TextField()

    def getRelatedTemplate(self):
        print("text template name")
        return "snugget_text.html"

    def __str__(self):
        return str(self.content)[:100]


class EmbedSnugget(Snugget):
    embed = EmbedVideoField()

    def getRelatedTemplate(self):
        print("embed template name")
        return "snugget_embed.html"

    def __str__(self):
        return "Embed Snugget: " + str(self.embed)
