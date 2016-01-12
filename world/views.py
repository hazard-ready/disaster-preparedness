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

            data = {}
            if snugget_content is not None:
                for key, values in snugget_content['groups'].items():
                    sections = {}
                    if values:
                        template = 'found_content.html'
                        heading = values[0].heading
                        for text_snugget in values:
                            sections[text_snugget.section] = text_snugget
                
                    data[key] = {
                        'heading': heading,
                        'sections': sections
                    }

        return render(request, template, {
            'location': location,
            'settings': settings,
            'data': data,
        })


    # if not, we'll still serve up the same template without data
    else:
        return render(request, 'index.html', {
            'location': location,
            'settings': settings
            })
