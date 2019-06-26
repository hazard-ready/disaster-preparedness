import math
import os
import sys
from django.contrib.gis.gdal import GDALRaster
from django.contrib.gis.geos import Polygon
from django.contrib.gis.utils import LayerMapping


# The width & height to tile rasters to.
# Empirically, tile sizes as large as 8053 work, while 10000 hits a memory overflow bug in either Django or GDAL and crashes.
# However, smaller tiles give us faster lookups, while really small (e.g. 10) make the data load interminably slow.
rasterTileSize = 128


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

RDPO_Lsd_Clark_mapping = {
    'lookup_val': 'lookup_val',
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
RDPO_Lsd_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_Lsd_Clark.shp'))
Wildfire_risk_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/Wildfire_risk.tif'))
RDPOCascadiaM9_3_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_3_Clark.shp'))
casceq_m9pgv1_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/casceq_m9pgv1.tif'))
RDPO_region_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region.shp'))
RDPOCascadiaM9_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_OR.shp'))
OR_lsd_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/OR_lsd.tif'))
# END OF GENERATED CODE BLOCK
######################################################

def tileLoadRaster(model, filename, band=0):
    tilesLoaded = 0
    tilesSkipped = 0
    model.objects.all().delete()
    sourceRaster = GDALRaster(filename, write=True)
    xTiles = math.ceil(sourceRaster.width / rasterTileSize)
    yTiles = math.ceil(sourceRaster.height / rasterTileSize)
    for x in range(0, xTiles):
      if x+1 != xTiles:
        width = rasterTileSize
      else:
        width = sourceRaster.width % rasterTileSize
      offsetX = x * rasterTileSize
      originX = sourceRaster.origin.x + offsetX * sourceRaster.scale.x
      for y in range(0, yTiles):
        if y+1 != yTiles:
          height = rasterTileSize
        else:
          height = sourceRaster.height % rasterTileSize
        offsetY = y * rasterTileSize
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
              }],
              'datatype': 1 # GDT_Byte aka 8-bit unsigned integer
            })
        )
        if rasterTile.rast.bands[band].min is None:
            # This situation causes GDAL to print 2 lines of error code to the console, which are always safe to ignore, so we can use ANSI escape sequences to clean that up
            sys.stdout.write("\033[F\033[K")
            print("Skipping tile (" + str(x) + ", " + str(y) + ")\twith origin (" + str(originX)[:9] + ", " + str(originY)[:9] + ")\tdue to lack of data. It's safe to ignore 'no valid pixels' GDAL_ERRORs in conjunction with this.")
            sys.stdout.write("\033[F\033[F\033[K")
            tilesSkipped += 1
        else:
            sys.stdout.write('.')
            rasterTile.bbox=Polygon.from_bbox(rasterTile.rast.extent)
            rasterTile.save()
            tilesLoaded += 1
        if x == 0:
            sys.stdout.flush() # make sure output shows up at least once per column
    print("\t...loaded", str(tilesLoaded), "tiles and skipped", str(tilesSkipped), "because they contained only NODATA pixels.")
    # clear remaining detritus from GDAL_ERRORs
    print("                                                                                          ")
    sys.stdout.write("\033[F\033[K")




def run(verbose=True):

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadGroups
    from .models import ShapefileGroup
    RDPOLiquefact_Clark = ShapefileGroup.objects.get_or_create(name='RDPOLiquefact_Clark')
    RDPO_counties = ShapefileGroup.objects.get_or_create(name='RDPO_counties')
    RDPOLiquefaction_OR = ShapefileGroup.objects.get_or_create(name='RDPOLiquefaction_OR')
    RDPO_Lsd_Clark = ShapefileGroup.objects.get_or_create(name='RDPO_Lsd_Clark')
    Wildfire_risk = ShapefileGroup.objects.get_or_create(name='Wildfire_risk')
    RDPOCascadiaM9_3_Clark = ShapefileGroup.objects.get_or_create(name='RDPOCascadiaM9_3_Clark')
    casceq_m9pgv1 = ShapefileGroup.objects.get_or_create(name='casceq_m9pgv1')
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

    print('Loading data for RDPO_Lsd_Clark')
    from .models import RDPO_Lsd_Clark
    lm_RDPO_Lsd_Clark = LayerMapping(RDPO_Lsd_Clark, RDPO_Lsd_Clark_shp, RDPO_Lsd_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_Lsd_Clark.save()

    print('Loading data for Wildfire_risk')
    from .models import Wildfire_risk
    tileLoadRaster(Wildfire_risk, Wildfire_risk_tif)

    print('Loading data for RDPOCascadiaM9_3_Clark')
    from .models import RDPOCascadiaM9_3_Clark
    lm_RDPOCascadiaM9_3_Clark = LayerMapping(RDPOCascadiaM9_3_Clark, RDPOCascadiaM9_3_Clark_shp, RDPOCascadiaM9_3_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOCascadiaM9_3_Clark.save()

    print('Loading data for casceq_m9pgv1')
    from .models import casceq_m9pgv1
    tileLoadRaster(casceq_m9pgv1, casceq_m9pgv1_tif)

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

    print("Data load finished.  GDAL_ERROR 'Failed to compute statistics, no valid pixels found in sampling' is safe to ignore if the data includes any raster files with any NODATA pixels.")

