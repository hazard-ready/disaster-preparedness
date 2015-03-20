from django.shortcuts import render
from django.contrib.gis.geos import Point
from itertools import chain
from .models import TsunamiZone
from .models import WorldBorder

# Create your views here.
def zoneCheck(request):
    lat = -123.9125932
    lng = 45.9928274
    pnt = Point(lat, lng)    
    qs_w = WorldBorder.objects.filter(mpoly__contains=pnt);
    qs_t = TsunamiZone.objects.filter(geom__contains=pnt);
    
    zonesStrings = list(chain(qs_w, qs_t));
    context = {'lat': lat, 'lng': lng, 'areas': zonesStrings}
    return render(request, 'zonecheck.html', context)