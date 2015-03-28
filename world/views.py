from django.shortcuts import render
from .models import *

def app_view(request):
  
  # if user submitted lat/lng, find our snuggets and send them to our template
  if 'lat' and 'lng' in request.GET:

    lat = request.GET['lat']
    lng = request.GET['lng']

    if len(lat) > 0:
    
      snugget_content = Snugget.findSnuggetsForPoint(lat=float(lng), lng=float(lat))    
        
      return render(request, 'index.html', {'data': snugget_content, 'lat':lat, 'lng':lng})    

  # if not, we'll still serve up the same template without data
  else:

    return render(request, 'index.html')
