import os
from django.contrib.gis.utils import LayerMapping


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
RDPOCascadiaM9_3_Clark_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_3_Clark.shp'))
RDPO_region_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPO_region.shp'))
RDPOCascadiaM9_OR_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../disasterinfosite/data/simplified/RDPOCascadiaM9_OR.shp'))
# END OF GENERATED CODE BLOCK
######################################################


def run(verbose=True):

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadGroups
    from .models import ShapefileGroup
    quake = ShapefileGroup.objects.get_or_create(name='quake')
# END OF GENERATED CODE BLOCK
######################################################

######################################################
# GENERATED CODE GOES HERE
# DO NOT MANUALLY EDIT CODE IN THIS SECTION - IT WILL BE OVERWRITTEN
# loadImports
    print('Loading data for RDPOLiquefact_Clark')
    from .models import RDPOLiquefact_Clark
    lm_RDPOLiquefact_Clark = LayerMapping(RDPOLiquefact_Clark, RDPOLiquefact_Clark_shp, RDPOLiquefact_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOLiquefact_Clark.save(strict=True, verbose=verbose)

    print('Loading data for RDPO_counties')
    from .models import RDPO_counties
    lm_RDPO_counties = LayerMapping(RDPO_counties, RDPO_counties_shp, RDPO_counties_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_counties.save(strict=True, verbose=verbose)

    print('Loading data for RDPOLiquefaction_OR')
    from .models import RDPOLiquefaction_OR
    lm_RDPOLiquefaction_OR = LayerMapping(RDPOLiquefaction_OR, RDPOLiquefaction_OR_shp, RDPOLiquefaction_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOLiquefaction_OR.save(strict=True, verbose=verbose)

    print('Loading data for RDPOCascadiaM9_3_Clark')
    from .models import RDPOCascadiaM9_3_Clark
    lm_RDPOCascadiaM9_3_Clark = LayerMapping(RDPOCascadiaM9_3_Clark, RDPOCascadiaM9_3_Clark_shp, RDPOCascadiaM9_3_Clark_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOCascadiaM9_3_Clark.save(strict=True, verbose=verbose)

    print('Loading data for RDPO_region')
    from .models import RDPO_region
    lm_RDPO_region = LayerMapping(RDPO_region, RDPO_region_shp, RDPO_region_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPO_region.save(strict=True, verbose=verbose)

    print('Loading data for RDPOCascadiaM9_OR')
    from .models import RDPOCascadiaM9_OR
    lm_RDPOCascadiaM9_OR = LayerMapping(RDPOCascadiaM9_OR, RDPOCascadiaM9_OR_shp, RDPOCascadiaM9_OR_mapping, transform=True, encoding='UTF-8', unique=['lookup_val'])
    lm_RDPOCascadiaM9_OR.save(strict=True, verbose=verbose)

# END OF GENERATED CODE BLOCK
######################################################

    print('Data load finished.')

