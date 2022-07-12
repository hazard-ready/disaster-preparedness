import math
import os
import sys
from django.contrib.gis.gdal import GDALRaster
from django.contrib.gis.geos import Polygon
from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand
from disasterinfosite.settings import BASE_DIR

# The width & height to tile rasters to.
# Empirically, tile sizes as large as 8053 work, while 10000 hits a memory overflow bug in either Django or GDAL and crashes.
# However, smaller tiles give us faster lookups, while really small (e.g. 10) make the data load interminably slow.
rasterTileSize = 128


######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadMappings
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
                    'datatype': 1  # GDT_Byte aka 8-bit unsigned integer
                })
            )
            if rasterTile.rast.bands[band].min is None:
                # This situation causes GDAL to print 2 lines of error code to the console, which are always safe to ignore, so we can use ANSI escape sequences to clean that up
                sys.stdout.write("\033[F\033[K")
                print("Skipping tile (" + str(x) + ", " + str(y) + ")\twith origin (" + str(originX)[:9] + ", " + str(originY)[
                      :9] + ")\tdue to lack of data. It's safe to ignore 'no valid pixels' GDAL_ERRORs in conjunction with this.")
                sys.stdout.write("\033[F\033[F\033[K")
                tilesSkipped += 1
            else:
                if y % 10 == 0:
                    sys.stdout.write('.')
                rasterTile.bbox = Polygon.from_bbox(rasterTile.rast.extent)
                rasterTile.save()
                tilesLoaded += 1
            sys.stdout.flush()  # flush often because otherwise the ANSI escape sequence "cleverness" becomes clumsiness when it goes out of sync
    print("\t...loaded", str(tilesLoaded), "tiles and skipped", str(
        tilesSkipped), "because they contained only NODATA pixels.")
    # clear remaining detritus from GDAL_ERRORs
    print("                                                                                          ")
    sys.stdout.write("\033[F\033[K")


def run(verbose=True):

    ######################################################
    # GENERATED CODE GOES HERE
    # DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
    # loadGroups
    # END OF GENERATED CODE BLOCK
    ######################################################

    ######################################################
    # GENERATED CODE GOES HERE
    # DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
    # loadImports
    # END OF GENERATED CODE BLOCK
    ######################################################

    print("Data load finished.  GDAL_ERROR 'Failed to compute statistics, no valid pixels found in sampling' is safe to ignore if the data includes any raster files with any NODATA pixels.")


class Command(BaseCommand):
    help = """ Load data from the data directory """

    def handle(self, *args, **options):
        run()
