from django.shortcuts import render
from .models import *

def app_view(request):
  
  # if user submitted lat/lng, find our snuggets and send them to our template
  if 'lat' and 'lng' in request.GET:

    lat = request.GET['lat']
    lng = request.GET['lng']

    if len(lat) > 0:
    
      snugget_content = Snugget.findSnuggetsForPoint(lat=float(lat), lng=float(lng))    
        
      return render(request, 'index.html', {'data': snugget_content, 'has_location':True})

  # if not, we'll still serve up the same template without data
  else:

    return render(request, 'index.html', {'has_location':False})
