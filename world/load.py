import os
from django.contrib.gis.utils import LayerMapping

# Auto-generated `LayerMapping` dictionary for TsunamiZone model,
# modified later by cool devs.
tsunamizone_mapping = {
    'type': 'Type',
    'typeid': 'typeID',
    'geom': 'MULTIPOLYGON',
}

impactzone_mapping = {
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'zoneid': 'zoneID',
    'zone': 'zone',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for ExpectedGroundShaking model
expectedgroundshaking_mapping = {
    'rate': 'gridcode',
    'shaking': 'Intensity',
    'geom': 'MULTIPOLYGON',
}

landslidedeformation_mapping = {
    'score': 'GRIDCODE',
    'label': 'PGD_Class',
    'geom': 'MULTIPOLYGON',
}

liquefactiondeformation_mapping = {
    'score': 'gridcode',
    'label': 'PGD_Class',
    'geom': 'MULTIPOLYGON',
}

tsunami_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/tsunamiZone_simple.shp'))
impact_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/new_Impact_Zones_Simple.shp'))
groundshaking_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/GroundShaking_simple.shp'))
landslide_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Landslide_simple.shp'))
liquefaction_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Liquefaction_simple.shp'))


def run(verbose=True):
    "Making stuff happen but this line is here because some/all stuff below here might get commented out."

    from .models import TsunamiZone
    lm2 = LayerMapping(TsunamiZone, tsunami_shp, tsunamizone_mapping,
                   transform=True, encoding='iso-8859-1',
                   unique=['typeid'])
    lm2.save(strict=True, verbose=verbose)

    # from .models import ImpactZoneData
    # lm3 = LayerMapping(ImpactZoneData, impact_shp, impactzone_mapping,
    #                    transform=True, encoding='iso-8859-1',
    #                    unique=['zoneid'])
    # lm3.save(strict=True, verbose=verbose)

    # from .models import ExpectedGroundShaking
    # lm4 = LayerMapping(ExpectedGroundShaking, groundshaking_shp, expectedgroundshaking_mapping,
    #                   transform=True, encoding='iso-8859-1',
    #                   unique=['rate'])
    # lm4.save(strict=True, verbose=verbose)

    # from .models import LandslideDeformation
    # lm5 = LayerMapping(LandslideDeformation, landslide_shp, landslidedeformation_mapping,
    #                  transform=True, encoding='iso-8859-1',
    #                  unique=['score'])
    # lm5.save(strict=True, verbose=verbose)

    # from .models import LiquefactionDeformation
    # lm6 = LayerMapping(LiquefactionDeformation, liquefaction_shp, liquefactiondeformation_mapping,
    #                   transform=True, encoding='iso-8859-1',
    #                   unique=['score'])
    # lm6.save(strict=True, verbose=verbose)
