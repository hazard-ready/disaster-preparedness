from django.contrib.gis.db import models


zoneOptions = {
                1: 'Eastern',
                2: 'Valley',
                3: 'Coastal',
                4: 'Tsunami',
                }

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
class ImpactZone(models.Model):
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
        label = "Impact Zone: " + zoneName + "(perim: " + str(self.perimeter) + " orbndy24: " + str(self.orbndy24) + " orbndy24i: " + str(self.orbndy24i) + ")"
        return label