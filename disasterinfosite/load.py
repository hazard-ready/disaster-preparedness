import os
from django.contrib.gis.utils import LayerMapping


######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadMappings
EQ_Fault_Buffer_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

EQ_Historic_Distance_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

EQ_Most_Like_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

EQ_Worst_Case_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

Fire_Hist_Bound_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

Fire_Intensity_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

Fire_Worst_Case_placeholder_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

Flood_Channel_Migration_Zones_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

Flood_FEMA_DFRIM_2015_mapping = {
    'femades': 'FEMADES',
    'geom': 'MULTIPOLYGON'
}

Flood_Worst_Case_ph_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}

Landslide_placeholder_mapping = {
    'lookup_val': 'lookup_val',
    'geom': 'MULTIPOLYGON'
}


EQ_Fault_Buffer_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/EQ_Fault_Buffer.shp'))
EQ_Historic_Distance_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/EQ_Historic_Distance.shp'))
EQ_Most_Like_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/EQ_Most_Like.shp'))
EQ_Worst_Case_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/EQ_Worst_Case.shp'))
Fire_Hist_Bound_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/Fire_Hist_Bound.shp'))
Fire_Intensity_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/Fire_Intensity.shp'))
Fire_Worst_Case_placeholder_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/Fire_Worst_Case_placeholder.shp'))
Flood_Channel_Migration_Zones_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/Flood_Channel_Migration_Zones.shp'))
Flood_FEMA_DFRIM_2015_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/Flood_FEMA_DFRIM_2015.shp'))
Flood_Worst_Case_ph_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/Flood_Worst_Case_ph.shp'))
Landslide_placeholder_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/Landslide_placeholder.shp'))
# END OF GENERATED CODE BLOCK
######################################################


def run(verbose=True):

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadImports
    from .models import EQ_Fault_Buffer
    lm_EQ_Fault_Buffer = LayerMapping(EQ_Fault_Buffer, EQ_Fault_Buffer_shp, EQ_Fault_Buffer_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_EQ_Fault_Buffer.save(strict=True, verbose=verbose)

    from .models import EQ_Historic_Distance
    lm_EQ_Historic_Distance = LayerMapping(EQ_Historic_Distance, EQ_Historic_Distance_shp, EQ_Historic_Distance_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_EQ_Historic_Distance.save(strict=True, verbose=verbose)

    from .models import EQ_Most_Like
    lm_EQ_Most_Like = LayerMapping(EQ_Most_Like, EQ_Most_Like_shp, EQ_Most_Like_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_EQ_Most_Like.save(strict=True, verbose=verbose)

    from .models import EQ_Worst_Case
    lm_EQ_Worst_Case = LayerMapping(EQ_Worst_Case, EQ_Worst_Case_shp, EQ_Worst_Case_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_EQ_Worst_Case.save(strict=True, verbose=verbose)

    from .models import Fire_Hist_Bound
    lm_Fire_Hist_Bound = LayerMapping(Fire_Hist_Bound, Fire_Hist_Bound_shp, Fire_Hist_Bound_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_Fire_Hist_Bound.save(strict=True, verbose=verbose)

    from .models import Fire_Intensity
    lm_Fire_Intensity = LayerMapping(Fire_Intensity, Fire_Intensity_shp, Fire_Intensity_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_Fire_Intensity.save(strict=True, verbose=verbose)

    from .models import Fire_Worst_Case_placeholder
    lm_Fire_Worst_Case_placeholder = LayerMapping(Fire_Worst_Case_placeholder, Fire_Worst_Case_placeholder_shp, Fire_Worst_Case_placeholder_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_Fire_Worst_Case_placeholder.save(strict=True, verbose=verbose)

    from .models import Flood_Channel_Migration_Zones
    lm_Flood_Channel_Migration_Zones = LayerMapping(Flood_Channel_Migration_Zones, Flood_Channel_Migration_Zones_shp, Flood_Channel_Migration_Zones_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_Flood_Channel_Migration_Zones.save(strict=True, verbose=verbose)

    from .models import Flood_FEMA_DFRIM_2015
    lm_Flood_FEMA_DFRIM_2015 = LayerMapping(Flood_FEMA_DFRIM_2015, Flood_FEMA_DFRIM_2015_shp, Flood_FEMA_DFRIM_2015_mapping, transform=True, encoding='UTF-8', unique=['femades'])
    lm_Flood_FEMA_DFRIM_2015.save(strict=True, verbose=verbose)

    from .models import Flood_Worst_Case_ph
    lm_Flood_Worst_Case_ph = LayerMapping(Flood_Worst_Case_ph, Flood_Worst_Case_ph_shp, Flood_Worst_Case_ph_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_Flood_Worst_Case_ph.save(strict=True, verbose=verbose)

    from .models import Landslide_placeholder
    lm_Landslide_placeholder = LayerMapping(Landslide_placeholder, Landslide_placeholder_shp, Landslide_placeholder_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_Landslide_placeholder.save(strict=True, verbose=verbose)

# END OF GENERATED CODE BLOCK
######################################################

