import math
import os
import sys
from django.contrib.gis.gdal import GDALRaster
from django.contrib.gis.geos import Polygon
from django.contrib.gis.utils import LayerMapping


# If a raster's height or width is > this threshold, tile it
# In theory this can be up to INT_MAX * 2, but that runs into memory constraints
rasterTileSize = 5000


######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadMappings
# END OF GENERATED CODE BLOCK
######################################################

def tileLoadRaster(model, filename, band=0):
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
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            print("Skipping tile\t(" + str(x) + ", " + str(y) + ") with \tOrigin (" + str(originX) + ", " + str(originY) + ") due to lack of data.\tIt's safe to ignore the GDAL_ERROR above this line.")
        else:
            sys.stdout.write('.')
            if x == 0:
                sys.stdout.flush() # make sure output shows up at least once per column
            rasterTile.bbox=Polygon.from_bbox(rasterTile.rast.extent)
            rasterTile.save()




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

    print('Data load finished.')

