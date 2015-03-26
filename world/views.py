from django.shortcuts import render
from django.contrib.gis.geos import Point
from itertools import chain
from .models import *

# Create your views here.
def zoneCheck(request):
    lat = -123.9125932
    lng = 45.9928274
    pnt = Point(lat, lng)    
    qs_t = TsunamiZone.objects.filter(geom__contains=pnt);
    qs_i = ImpactZoneData.objects.filter(geom__contains=pnt);
    qs_s = ExpectedGroundShaking.objects.filter(geom__contains=pnt);

    zonesStrings = list(chain(qs_t, qs_i, qs_s));
    context = {'lat': lat, 'lng': lng, 'areas': zonesStrings}
    return render(request, 'zonecheck.html', context)