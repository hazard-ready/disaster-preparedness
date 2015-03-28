import os
from django.contrib.gis.utils import LayerMapping

from .models import TsunamiZone
from .models import ImpactZoneData
from .models import ExpectedGroundShaking
from .models import LandslideDeformation
from .models import LiquefactionDeformation

# Auto-generated `LayerMapping` dictionary for TsunamiZone model,
# modified later by cool devs.
tsunamizone_mapping = {
    'type' : 'Type',
    'typeid' : 'typeID',
    'geom' : 'MULTIPOLYGON',
}

impactzone_mapping = {
    'area' : 'AREA',
    'perimeter': 'PERIMETER',
    'orbndy24' : 'ORBNDY24_',
    'orbndy24i' : 'ORBNDY24_I',
    'subjstate' : 'SUBJ_STATE',
    'feature': 'FEATURE',
    'geom' : 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for ExpectedGroundShaking model
expectedgroundshaking_mapping = {
    'rate' : 'gridcode', # Changed because attribute names changed in new shapefiles
    'shaking' : 'Intensity', # Changed because attribute names changed in new shapefiles
    'geom' : 'MULTIPOLYGON',
}

landslidedeformation_mapping = {
    'score' : 'GRIDCODE',
    'label' : 'PGD_Class',
    'geom' : 'MULTIPOLYGON',
}

liquefactiondeformation_mapping = {
    'score' : 'gridcode',
    'label' : 'PGD_Class',
    'geom' : 'MULTIPOLYGON',
}

tsunami_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/tsunamiZone_simple.shp'))
impact_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/ORP_Impact_Zones.shp'))
groundshaking_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/GroundShaking_simple.shp')) #Changed as per filename of updated shapefile
landslide_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Landslide_simple.shp')) #Changed as per filename of updated shapefile
liquefaction_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Liquefaction_simple.shp')) #Changed as per filename of updated shapefile

def run(verbose=True):
    "Making stuff happen but this line is here because some/all stuff below here might get commented out."

    lm2 = LayerMapping(TsunamiZone, tsunami_shp, tsunamizone_mapping,
                    transform=True, encoding='iso-8859-1',
                    unique=['typeid'])
    lm2.save(strict=True, verbose=verbose)

    #lm3 = LayerMapping(ImpactZoneData, impact_shp, impactzone_mapping,
    #                  transform=True, encoding='iso-8859-1',
    #                  unique=['area', 'perimeter', 'orbndy24', 'orbndy24i', 'subjstate', 'feature', 'geom'])
    #lm3.save(strict=True, verbose=verbose)


    #lm4 = LayerMapping(ExpectedGroundShaking, groundshaking_shp, expectedgroundshaking_mapping,
    #                   transform=True, encoding='iso-8859-1',
    #                   unique=['rate'])
    #lm4.save(strict=True, verbose=verbose)

    #lm5 = LayerMapping(LandslideDeformation, landslide_shp, landslidedeformation_mapping,
    #                  transform=True, encoding='iso-8859-1',
    #                  unique=['score'])
    #lm5.save(strict=True, verbose=verbose)

    #lm6 = LayerMapping(LiquefactionDeformation, liquefaction_shp, liquefactiondeformation_mapping,
    #                   transform=True, encoding='iso-8859-1',
    #                   unique=['score'])
    #lm6.save(strict=True, verbose=verbose)
