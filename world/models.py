from django.contrib.gis.db import models

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.name

# This is an auto-generated Django model module created by ogrinspect.
class TsunamiZone(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=80)
    type = models.CharField(max_length=50)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()
    
        # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.name

# This is an auto-generated Django model module created by ogrinspect.
class ImpactZone(models.Model):
    area = models.IntegerField()
    perimeter = models.IntegerField()
    orbndy24 = models.IntegerField()
    orbndy24i = models.IntegerField()
    subjstate = models.CharField(max_length=50)
    feature = models.IntegerField() #This is the field that tells us which DOGAMI designated zone.
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __str__(self):
        return str(self.feature)