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
RDPO_region_quake_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_region_winter_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_Lsd_Clark_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_quake_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOflood_OR_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_volcano_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_region_summer_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOFire_Clark_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_region_fire_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOCascadiaM9_3_Clark_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_region_volcano_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOLiquefaction_OR_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOflood_clark_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_region_flood_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOvolcanoes_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_winter_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_fire_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_WA_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_flood_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_OR_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_region_slide_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOCascadiaM9_OR_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOLiquefact_Clark_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_summer_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPOhistflood_mapping = {
    'lookup_val': 'Lookup_val',
    'geom': 'MULTIPOLYGON'
}

RDPO_counties_slide_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}


RDPO_region_quake_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region_quake.shp'))
RDPO_region_winter_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region_winter.shp'))
RDPO_Lsd_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_Lsd_Clark.shp'))
RDPO_counties_quake_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties_quake.shp'))
RDPOflood_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOflood_OR.shp'))
RDPO_counties_volcano_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties_volcano.shp'))
RDPO_Lsld_OR_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/RDPO_Lsld_OR.tif'))
RDPOFire_Clark_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/RDPOFire_Clark.tif'))
RDPO_region_summer_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region_summer.shp'))
RDPO_region_fire_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region_fire.shp'))
RDPOCascadiaM9_3_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_3_Clark.shp'))
RDPOFire_OR_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/RDPOFire_OR.tif'))
RDPO_region_volcano_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region_volcano.shp'))
RDPOLiquefaction_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOLiquefaction_OR.shp'))
RDPOCascadiaM9_Col_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/RDPOCascadiaM9_Col.tif'))
RDPOflood_clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOflood_clark.shp'))
RDPO_region_flood_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region_flood.shp'))
RDPOvolcanoes_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOvolcanoes.shp'))
RDPO_counties_winter_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties_winter.shp'))
RDPO_counties_fire_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties_fire.shp'))
RDPO_WA_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_WA.shp'))
RDPO_counties_flood_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties_flood.shp'))
RDPO_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_OR.shp'))
RDPOCascadiaM9_3Cnty_tif = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/reprojected/RDPOCascadiaM9_3Cnty.tif'))
RDPO_region_slide_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region_slide.shp'))
RDPOCascadiaM9_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_OR.shp'))
RDPOLiquefact_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOLiquefact_Clark.shp'))
RDPO_counties_summer_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties_summer.shp'))
RDPOhistflood_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOhistflood.shp'))
RDPO_counties_slide_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_counties_slide.shp'))
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
    quake = ShapefileGroup.objects.get_or_create(name='quake')
    winter = ShapefileGroup.objects.get_or_create(name='winter')
    slide = ShapefileGroup.objects.get_or_create(name='slide')
    flood = ShapefileGroup.objects.get_or_create(name='flood')
    volcano = ShapefileGroup.objects.get_or_create(name='volcano')
    fire = ShapefileGroup.objects.get_or_create(name='fire')
    summer = ShapefileGroup.objects.get_or_create(name='summer')
# END OF GENERATED CODE BLOCK
######################################################

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadImports
    print('Loading data for RDPO_region_quake')
    from .models import RDPO_region_quake
    lm_RDPO_region_quake = LayerMapping(RDPO_region_quake, RDPO_region_quake_shp, RDPO_region_quake_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region_quake.save()

    print('Loading data for RDPO_region_winter')
    from .models import RDPO_region_winter
    lm_RDPO_region_winter = LayerMapping(RDPO_region_winter, RDPO_region_winter_shp, RDPO_region_winter_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region_winter.save()

    print('Loading data for RDPO_Lsd_Clark')
    from .models import RDPO_Lsd_Clark
    lm_RDPO_Lsd_Clark = LayerMapping(RDPO_Lsd_Clark, RDPO_Lsd_Clark_shp, RDPO_Lsd_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_Lsd_Clark.save()

    print('Loading data for RDPO_counties_quake')
    from .models import RDPO_counties_quake
    lm_RDPO_counties_quake = LayerMapping(RDPO_counties_quake, RDPO_counties_quake_shp, RDPO_counties_quake_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties_quake.save()

    print('Loading data for RDPOflood_OR')
    from .models import RDPOflood_OR
    lm_RDPOflood_OR = LayerMapping(RDPOflood_OR, RDPOflood_OR_shp, RDPOflood_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOflood_OR.save()

    print('Loading data for RDPO_counties_volcano')
    from .models import RDPO_counties_volcano
    lm_RDPO_counties_volcano = LayerMapping(RDPO_counties_volcano, RDPO_counties_volcano_shp, RDPO_counties_volcano_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties_volcano.save()

    print('Loading data for RDPO_Lsld_OR')
    from .models import RDPO_Lsld_OR
    tileLoadRaster(RDPO_Lsld_OR, RDPO_Lsld_OR_tif)

    print('Loading data for RDPOFire_Clark')
    from .models import RDPOFire_Clark
    tileLoadRaster(RDPOFire_Clark, RDPOFire_Clark_tif)

    print('Loading data for RDPO_region_summer')
    from .models import RDPO_region_summer
    lm_RDPO_region_summer = LayerMapping(RDPO_region_summer, RDPO_region_summer_shp, RDPO_region_summer_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region_summer.save()

    print('Loading data for RDPO_region_fire')
    from .models import RDPO_region_fire
    lm_RDPO_region_fire = LayerMapping(RDPO_region_fire, RDPO_region_fire_shp, RDPO_region_fire_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region_fire.save()

    print('Loading data for RDPOCascadiaM9_3_Clark')
    from .models import RDPOCascadiaM9_3_Clark
    lm_RDPOCascadiaM9_3_Clark = LayerMapping(RDPOCascadiaM9_3_Clark, RDPOCascadiaM9_3_Clark_shp, RDPOCascadiaM9_3_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOCascadiaM9_3_Clark.save()

    print('Loading data for RDPOFire_OR')
    from .models import RDPOFire_OR
    tileLoadRaster(RDPOFire_OR, RDPOFire_OR_tif)

    print('Loading data for RDPO_region_volcano')
    from .models import RDPO_region_volcano
    lm_RDPO_region_volcano = LayerMapping(RDPO_region_volcano, RDPO_region_volcano_shp, RDPO_region_volcano_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region_volcano.save()

    print('Loading data for RDPOLiquefaction_OR')
    from .models import RDPOLiquefaction_OR
    lm_RDPOLiquefaction_OR = LayerMapping(RDPOLiquefaction_OR, RDPOLiquefaction_OR_shp, RDPOLiquefaction_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOLiquefaction_OR.save()

    print('Loading data for RDPOCascadiaM9_Col')
    from .models import RDPOCascadiaM9_Col
    tileLoadRaster(RDPOCascadiaM9_Col, RDPOCascadiaM9_Col_tif)

    print('Loading data for RDPOflood_clark')
    from .models import RDPOflood_clark
    lm_RDPOflood_clark = LayerMapping(RDPOflood_clark, RDPOflood_clark_shp, RDPOflood_clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOflood_clark.save()

    print('Loading data for RDPO_region_flood')
    from .models import RDPO_region_flood
    lm_RDPO_region_flood = LayerMapping(RDPO_region_flood, RDPO_region_flood_shp, RDPO_region_flood_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region_flood.save()

    print('Loading data for RDPOvolcanoes')
    from .models import RDPOvolcanoes
    lm_RDPOvolcanoes = LayerMapping(RDPOvolcanoes, RDPOvolcanoes_shp, RDPOvolcanoes_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOvolcanoes.save()

    print('Loading data for RDPO_counties_winter')
    from .models import RDPO_counties_winter
    lm_RDPO_counties_winter = LayerMapping(RDPO_counties_winter, RDPO_counties_winter_shp, RDPO_counties_winter_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties_winter.save()

    print('Loading data for RDPO_counties_fire')
    from .models import RDPO_counties_fire
    lm_RDPO_counties_fire = LayerMapping(RDPO_counties_fire, RDPO_counties_fire_shp, RDPO_counties_fire_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties_fire.save()

    print('Loading data for RDPO_WA')
    from .models import RDPO_WA
    lm_RDPO_WA = LayerMapping(RDPO_WA, RDPO_WA_shp, RDPO_WA_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_WA.save()

    print('Loading data for RDPO_counties_flood')
    from .models import RDPO_counties_flood
    lm_RDPO_counties_flood = LayerMapping(RDPO_counties_flood, RDPO_counties_flood_shp, RDPO_counties_flood_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties_flood.save()

    print('Loading data for RDPO_OR')
    from .models import RDPO_OR
    lm_RDPO_OR = LayerMapping(RDPO_OR, RDPO_OR_shp, RDPO_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_OR.save()

    print('Loading data for RDPOCascadiaM9_3Cnty')
    from .models import RDPOCascadiaM9_3Cnty
    tileLoadRaster(RDPOCascadiaM9_3Cnty, RDPOCascadiaM9_3Cnty_tif)

    print('Loading data for RDPO_region_slide')
    from .models import RDPO_region_slide
    lm_RDPO_region_slide = LayerMapping(RDPO_region_slide, RDPO_region_slide_shp, RDPO_region_slide_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region_slide.save()

    print('Loading data for RDPOCascadiaM9_OR')
    from .models import RDPOCascadiaM9_OR
    lm_RDPOCascadiaM9_OR = LayerMapping(RDPOCascadiaM9_OR, RDPOCascadiaM9_OR_shp, RDPOCascadiaM9_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOCascadiaM9_OR.save()

    print('Loading data for RDPOLiquefact_Clark')
    from .models import RDPOLiquefact_Clark
    lm_RDPOLiquefact_Clark = LayerMapping(RDPOLiquefact_Clark, RDPOLiquefact_Clark_shp, RDPOLiquefact_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOLiquefact_Clark.save()

    print('Loading data for RDPO_counties_summer')
    from .models import RDPO_counties_summer
    lm_RDPO_counties_summer = LayerMapping(RDPO_counties_summer, RDPO_counties_summer_shp, RDPO_counties_summer_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties_summer.save()

    print('Loading data for RDPOhistflood')
    from .models import RDPOhistflood
    lm_RDPOhistflood = LayerMapping(RDPOhistflood, RDPOhistflood_shp, RDPOhistflood_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOhistflood.save()

    print('Loading data for RDPO_counties_slide')
    from .models import RDPO_counties_slide
    lm_RDPO_counties_slide = LayerMapping(RDPO_counties_slide, RDPO_counties_slide_shp, RDPO_counties_slide_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties_slide.save()

# END OF GENERATED CODE BLOCK
######################################################

    print("Data load finished.  GDAL_ERROR 'Failed to compute statistics, no valid pixels found in sampling' is safe to ignore if the data includes any raster files with any NODATA pixels.")

