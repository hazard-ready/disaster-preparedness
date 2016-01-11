import os
from django.contrib.gis.utils import LayerMapping


######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadMappings
EQ_Fault_Buffer_mapping = {
    'snugget_id': 'snugget_ID',
    'geom': 'MULTIPOLYGON'
}

EQ_GroundShaking_MostLike_mapping = {
    'intensity': 'Intensity',
    'geom': 'MULTIPOLYGON'
}

EQ_Historic_Distance_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

Fire_hist_nrocky_1889_2003_all_mapping = {
    'lookup_val': 'lookup_val',
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


EQ_Fault_Buffer_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/EQ_Fault_Buffer.shp'))
EQ_GroundShaking_MostLike_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/EQ_GroundShaking_MostLike.shp'))
EQ_Historic_Distance_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/EQ_Historic_Distance.shp'))
Fire_hist_nrocky_1889_2003_all_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/Fire_hist_nrocky_1889_2003_all.shp'))
Flood_FEMA_DFIRM_2015_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/Flood_FEMA_DFIRM_2015.shp'))
MT_groundshaking_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../world/data/simplified/MT_groundshaking.shp'))
# END OF GENERATED CODE BLOCK
######################################################


def run(verbose=True):

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadImports
    from .models import EQ_Fault_Buffer
    lm_EQ_Fault_Buffer = LayerMapping(EQ_Fault_Buffer, EQ_Fault_Buffer_shp, EQ_Fault_Buffer_mapping, transform=True, encoding='UTF-8', unique=['snugget_id'])
    lm_EQ_Fault_Buffer.save(strict=True, verbose=verbose)

    from .models import EQ_GroundShaking_MostLike
    lm_EQ_GroundShaking_MostLike = LayerMapping(EQ_GroundShaking_MostLike, EQ_GroundShaking_MostLike_shp, EQ_GroundShaking_MostLike_mapping, transform=True, encoding='UTF-8', unique=['intensity'])
    lm_EQ_GroundShaking_MostLike.save(strict=True, verbose=verbose)

    from .models import EQ_Historic_Distance
    lm_EQ_Historic_Distance = LayerMapping(EQ_Historic_Distance, EQ_Historic_Distance_shp, EQ_Historic_Distance_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_EQ_Historic_Distance.save(strict=True, verbose=verbose)

    from .models import Fire_hist_nrocky_1889_2003_all
    lm_Fire_hist_nrocky_1889_2003_all = LayerMapping(Fire_hist_nrocky_1889_2003_all, Fire_hist_nrocky_1889_2003_all_shp, Fire_hist_nrocky_1889_2003_all_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_Fire_hist_nrocky_1889_2003_all.save(strict=True, verbose=verbose)

    from .models import Flood_FEMA_DFIRM_2015
    lm_Flood_FEMA_DFIRM_2015 = LayerMapping(Flood_FEMA_DFIRM_2015, Flood_FEMA_DFIRM_2015_shp, Flood_FEMA_DFIRM_2015_mapping, transform=True, encoding='UTF-8', unique=['femades'])
    lm_Flood_FEMA_DFIRM_2015.save(strict=True, verbose=verbose)

    from .models import MT_groundshaking
    lm_MT_groundshaking = LayerMapping(MT_groundshaking, MT_groundshaking_shp, MT_groundshaking_mapping, transform=True, encoding='UTF-8', unique=['intensity'])
    lm_MT_groundshaking.save(strict=True, verbose=verbose)

# END OF GENERATED CODE BLOCK
######################################################

