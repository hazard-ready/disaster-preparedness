from django.shortcuts import render
from .models import Snugget


def app_view(request):

    # if user submitted lat/lng, find our snuggets and send them to our template
    if 'lat' and 'lng' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']

        if len(lat) > 0:
            snugget_content = Snugget.findSnuggetsForPoint(lat=float(lat), lng=float(lng))
            snugget_content['structured'] = {
                'moment': {},
                'recovery': {},
                'prepare': {}
                }

            # Make our lives easier by additionally sorting these snugs into our 3 sections.
            for groupkey, group in snugget_content['groups'].items():
                snugget_content['structured']['moment'].setdefault(groupkey, [])
                snugget_content['structured']['recovery'].setdefault(groupkey, [])
                snugget_content['structured']['prepare'].setdefault(groupkey, [])

                for snugget in group:
                    if snugget.section.name == "The Moment":
                        snugget_content['structured']['moment'][groupkey].append(snugget)
                    elif snugget.section.name == "Community Recovery":
                        snugget_content['structured']['recovery'][groupkey].append(snugget)
                    elif snugget.section.name == "How To Prepare":
                        snugget_content['structured']['prepare'][groupkey].append(snugget)
                        
            return render(request, 'index.html', {'data': snugget_content, 'has_location': True})

    # if not, we'll still serve up the same template without data
    else:
        return render(request, 'index.html', {'has_location': False})
