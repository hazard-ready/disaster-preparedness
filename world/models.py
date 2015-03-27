from django.contrib.gis.db import models


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
    scenario_id = models.IntegerField() # 1 = local scenario, 2 = distant scenario
    location = models.CharField(max_length=80) # location and model grid name
    scenario_type = models.CharField(max_length=50) # local or distant
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()
    
    class Meta:
        unique_together = ('scenario_id', 'location')
    
        # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.location + " ("+ self.scenario_type + ")"

# This was an auto-generated Django model module created by ogrinspect with
# additional clarification by the devs.
# Our use of this data is primarily looking at the feature values.
# We don't care about other polygons in this data beyond those 4 impact zones.
class ImpactZoneData(models.Model):
    area = models.IntegerField()      # An area number.  Who knows.
    perimeter = models.IntegerField() # A permimiter number.  Who knows.
    orbndy24 = models.IntegerField()  # Value identifies source of boundary: BLM-generated lines, USFS Cartographic Feature File, USGS Digital Line Graph, WA Dept. of Natural Resources, BLM Geographic Coordinate Data Base, BLM Landline Layer, Other; FIPS codes used to identify counties if from a county, BLM's Western Oregon Digital Data Base 
    orbndy24i = models.IntegerField() # User Defined automatically generated numbers.
    subjstate = models.CharField(max_length=50) # User defined string.
    feature = models.IntegerField()   # This is the field that tells us which of the 4 DOGAMI designated zones it is (or 0 for other data) 
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        zoneName = zoneOptions.get(self.feature, 'Undefined zone')
        label = "Impact Zone Data: " + zoneName + "(perim: " + str(self.perimeter) + " orbndy24: " + str(self.orbndy24) + " orbndy24i: " + str(self.orbndy24i) + ")"
        return label
    
 # This is an auto-generated Django model module created by ogrinspect.
class ExpectedGroundShaking(models.Model):
    rate = models.IntegerField()
    shaking = models.CharField(max_length=11)
    geom = models.MultiPolygonField(srid=2991)
    objects = models.GeoManager()
    
    def __str__(self):
        return self.shaking + " (rate: " + str(self.rate) + ")"
    
class ImpactZone(models.Model):
    name = models.CharField(max_length=50)
    featureValue = models.IntegerField() # If/when ImpactZoneData gets cleaned up this could become a ForeignKey
    
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

class Snugget(models.Model):
    type = models.ForeignKey(SnuggetType, related_name='+', on_delete=models.PROTECT)
    shaking_filter = models.ForeignKey(ExpectedGroundShaking, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    impact_zone_filter = models.ForeignKey(ImpactZone, related_name='+', on_delete=models.PROTECT, blank=True, null=True)
    temp_text_field = models.TextField(null=True)
    # liquifaction_filter
    # landslide_filter
    
    section = models.ForeignKey(SnuggetSection, related_name='+', on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.type) + " Snugget for section " + str(self.section) + "  (impact zone: " + str(self.impact_zone_filter) + " shaking: " + str(self.shaking_filter) + ")"
    
    
class TextSnugget(models.Model):
    name = SNUGGET_TYPES[SNUG_TEXT]
    content = models.TextField()
    
    def __str__(self):
        return str(self.name)