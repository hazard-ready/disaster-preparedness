from django.shortcuts import render
from math import floor
from .models import Snugget, Location, SiteSettings


def app_view(request):
    location = Location.get_solo()
    settings = SiteSettings.get_solo()
    template = "no_content_found.html"

    # if user submitted lat/lng, find our snuggets and send them to our template
    if 'lat' and 'lng' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']

        if len(lat) > 0:
            snugget_content = Snugget.findSnuggetsForPoint(lat=float(lat), lng=float(lng))

            for keys, values in snugget_content['groups'].items():
                if values:
                    template = 'found_content.html'
                
        return render(request, template, {
            'location': location,
            'settings': settings,
            'data': snugget_content, 
        })


    # if not, we'll still serve up the same template without data
    else:
        return render(request, 'index.html', {
            'location': location,
            'settings': settings
            })