import os
from django.contrib.gis.utils import LayerMapping


######################################################
# Insert generated loadMappings here
######################################################
EQ_GroundShaking_MostLike_mapping = {
    'intensity': 'Intensity',
    'geom': 'MULTIPOLYGON'
}

Flood_FEMA_DFIRM_2015_mapping = {
    'femades': 'FEMADES',
    'geom': 'MULTIPOLYGON'
}

MT_groundshaking_mapping = {
    'intensity': 'intensity',
    'geom': 'MULTIPOLYGON'
}



######################################################
# Insert generated loadPaths here
######################################################

EQ_GroundShaking_MostLike_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/EQ_GroundShaking_MostLike.shp'))
Flood_FEMA_DFIRM_2015_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/Flood_FEMA_DFIRM_2015.shp'))
MT_groundshaking_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/MT_groundshaking.shp'))

def run(verbose=True):

######################################################
# Insert generated loadImports here
######################################################
    from .models import EQ_GroundShaking_MostLike
    lm_EQ_GroundShaking_MostLike = LayerMapping(EQ_GroundShaking_MostLike, EQ_GroundShaking_MostLike_shp, EQ_GroundShaking_MostLike_mapping, transform=True, encoding='UTF-8', unique=['intensity'])
    lm_EQ_GroundShaking_MostLike.save(strict=True, verbose=verbose)

    from .models import Flood_FEMA_DFIRM_2015
    lm_Flood_FEMA_DFIRM_2015 = LayerMapping(Flood_FEMA_DFIRM_2015, Flood_FEMA_DFIRM_2015_shp, Flood_FEMA_DFIRM_2015_mapping, transform=True, encoding='UTF-8', unique=['femades'])
    lm_Flood_FEMA_DFIRM_2015.save(strict=True, verbose=verbose)

    from .models import MT_groundshaking
    lm_MT_groundshaking = LayerMapping(MT_groundshaking, MT_groundshaking_shp, MT_groundshaking_mapping, transform=True, encoding='UTF-8', unique=['intensity'])
    lm_MT_groundshaking.save(strict=True, verbose=verbose)



