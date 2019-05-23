import math
import os
from django.contrib.gis.gdal import GDALRaster
from django.contrib.gis.geos import Polygon
from django.contrib.gis.utils import LayerMapping


# If a raster's height or width is > this threshold, tile it
# In theory this can be up to INT_MAX * 2, but that runs into memory constraints
rasterTileMaxDimension = 5000


######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadMappings
RDPOLiquefact_Clark_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOLiquefaction_OR_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOCascadiaM9_3_Clark_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_region_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOCascadiaM9_OR_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}



RDPOLiquefact_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOLiquefact_Clark.shp'))
RDPO_counties_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties.shp'))
RDPOLiquefaction_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOLiquefaction_OR.shp'))
RDPOCascadiaM9_3_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_3_Clark.shp'))
RDPO_region_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region.shp'))
RDPOCascadiaM9_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_OR.shp'))
OR_lsd_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/OR_lsd.tif'))
# END OF GENERATED CODE BLOCK
######################################################

def tileLoadRaster(model, filename, band=0):
    model.objects.all().delete()
    sourceRaster = GDALRaster(filename, write=True)
    xTiles = math.ceil(sourceRaster.width / rasterTileMaxDimension)
    yTiles = math.ceil(sourceRaster.height / rasterTileMaxDimension)
    for x in range(0, xTiles):
      if x+1 != xTiles:
        width = rasterTileMaxDimension
      else:
        width = sourceRaster.width % rasterTileMaxDimension
      offsetX = x * rasterTileMaxDimension
      originX = sourceRaster.origin.x + offsetX * sourceRaster.scale.x
      for y in range(0, yTiles):
        if y+1 != yTiles:
          height = rasterTileMaxDimension
        else:
          height = sourceRaster.height % rasterTileMaxDimension
        offsetY = y * rasterTileMaxDimension
        originY = sourceRaster.origin.y + offsetY * sourceRaster.scale.y
        rasterTile = model(
            rast=GDALRaster({
              'name': '/vsimem/tempraster',
              'srid': sourceRaster.srid,
              'width': width,
              'height': height,
              'origin': [originX, originY],
              'scale': sourceRaster.scale,
              'skew': sourceRaster.skew,
              'bands': [{
                'nodata_value': sourceRaster.bands[band].nodata_value,
                'data': sourceRaster.bands[band].data(
                  offset=(offsetX, offsetY),
                  size=(width, height)
                ),
                'size': (width, height),
                'offset': (0, 0)
              }]
            })
        )
        if rasterTile.rast.bands[band].min is None:
            print("...Skipping due to lack of data:\ttile (" + str(x) + ", " + str(y) + ")\tDimensions", str(width), "x", str(height), "\tOrigin (" + str(originX) + ", " + str(originY) + ").\tIt's safe to ignore the GDAL_ERROR above this line.")
        else:
            print("...Loading\ttile (" + str(x) + ", " + str(y) + ")\tDimensions", str(width), "x", str(height), "\tOrigin (" + str(originX) + ", " + str(originY) + ")")
            rasterTile.bbox=Polygon.from_bbox(rasterTile.rast.extent)
            rasterTile.save()




def run(verbose=True):

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadGroups
    from .models import ShapefileGroup
    RDPOLiquefact_Clark = ShapefileGroup.objects.get_or_create(name='RDPOLiquefact_Clark')
    RDPO_counties = ShapefileGroup.objects.get_or_create(name='RDPO_counties')
    RDPOLiquefaction_OR = ShapefileGroup.objects.get_or_create(name='RDPOLiquefaction_OR')
    RDPOCascadiaM9_3_Clark = ShapefileGroup.objects.get_or_create(name='RDPOCascadiaM9_3_Clark')
    RDPO_region = ShapefileGroup.objects.get_or_create(name='RDPO_region')
    RDPOCascadiaM9_OR = ShapefileGroup.objects.get_or_create(name='RDPOCascadiaM9_OR')
    OR_lsd = ShapefileGroup.objects.get_or_create(name='OR_lsd')
# END OF GENERATED CODE BLOCK
######################################################

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadImports
    print('Loading data for RDPOLiquefact_Clark')
    from .models import RDPOLiquefact_Clark
    lm_RDPOLiquefact_Clark = LayerMapping(RDPOLiquefact_Clark, RDPOLiquefact_Clark_shp, RDPOLiquefact_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOLiquefact_Clark.save()

    print('Loading data for RDPO_counties')
    from .models import RDPO_counties
    lm_RDPO_counties = LayerMapping(RDPO_counties, RDPO_counties_shp, RDPO_counties_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties.save()

    print('Loading data for RDPOLiquefaction_OR')
    from .models import RDPOLiquefaction_OR
    lm_RDPOLiquefaction_OR = LayerMapping(RDPOLiquefaction_OR, RDPOLiquefaction_OR_shp, RDPOLiquefaction_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOLiquefaction_OR.save()

    print('Loading data for RDPOCascadiaM9_3_Clark')
    from .models import RDPOCascadiaM9_3_Clark
    lm_RDPOCascadiaM9_3_Clark = LayerMapping(RDPOCascadiaM9_3_Clark, RDPOCascadiaM9_3_Clark_shp, RDPOCascadiaM9_3_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOCascadiaM9_3_Clark.save()

    print('Loading data for RDPO_region')
    from .models import RDPO_region
    lm_RDPO_region = LayerMapping(RDPO_region, RDPO_region_shp, RDPO_region_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region.save()

    print('Loading data for RDPOCascadiaM9_OR')
    from .models import RDPOCascadiaM9_OR
    lm_RDPOCascadiaM9_OR = LayerMapping(RDPOCascadiaM9_OR, RDPOCascadiaM9_OR_shp, RDPOCascadiaM9_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOCascadiaM9_OR.save()

    print('Loading data for OR_lsd')
    from .models import OR_lsd
    tileLoadRaster(OR_lsd, OR_lsd_tif)



# END OF GENERATED CODE BLOCK
######################################################

    print('Data load finished.')

