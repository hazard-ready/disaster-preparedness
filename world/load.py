import os
from django.contrib.gis.utils import LayerMapping

from .models import TsunamiZone
from .models import ImpactZone

# Auto-generated `LayerMapping` dictionary for TsunamiZone model,
# modified later by cool devs.
tsunamizone_mapping = {
    'scenario_id' : 'Id',
    'location' : 'Location',
    'scenario_type' : 'Type',
    'geom' : 'MULTIPOLYGON',
}

impactzone_mapping = {
    'area' : 'AREA',
    'perimeter': 'PERIMETER',
    'orbndy24' : 'ORBNDY24_',
    'orbndy24i' : 'ORBNDY24_I',
    'subjstate' : 'SUBJ_STATE',
    'feature': 'FEATURE',
    'geom' : 'Polygon',
}

tsunami_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/DOGAMI_TsunamiEvacuationZones_2013.shp'))
impact_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/ORP_Impact_zones.shp'))


def run(verbose=True):

    lm2 = LayerMapping(TsunamiZone, tsunami_shp, tsunamizone_mapping,
                      transform=True, encoding='iso-8859-1')
    lm2.save(strict=True, verbose=verbose)

    lm3 = LayerMapping(ImpactZone, impact_shp, impactzone_mapping,
                      transform=True, encoding='iso-8859-1')
    lm3.save(strict=True, verbose=verbose)


