from django.shortcuts import render
from collections import OrderedDict
from .models import Snugget, Location, SiteSettings, SupplyKit, ImportantLink, ShapefileGroup
from .fire_dial import make_icon

def app_view(request):
    location = Location.get_solo()
    important_links = ImportantLink.objects.all()
    settings = SiteSettings.get_solo()
    data_bounds = Location.get_data_bounds()
    supply_kit = SupplyKit.get_solo()
    supply_kit.meals = 3 * supply_kit.days
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
                            if not text_snugget.image:
                                text_snugget.dynamic_image = make_icon(text_snugget.percentage)
                            if not text_snugget.section in sections:
                                sections[text_snugget.section] = {}
                            if text_snugget.sub_section in sections[text_snugget.section]:
                                sections[text_snugget.section][text_snugget.sub_section].append(text_snugget)
                            else:
                                sections[text_snugget.section][text_snugget.sub_section] = [text_snugget]

                        for section, sub_section_dict in sections.items():
                            sections[section] = OrderedDict(sorted(sub_section_dict.items(), key=lambda t: t[0].order))

                        photos = []
                        for p in PastEventsPhoto.objects.filter(group=values[0].group):
                            photos.append(str(p))

                        data[key] = {
                            'heading': heading,
                            'sections': OrderedDict(sorted(sections.items(), key=lambda t: t[0].order )),
                            'likely_scenario_title': values[0].group.likely_scenario_title,
                            'likely_scenario_text': values[0].group.likely_scenario_text,
                            'photos': photos
                        }

        return render(request, template, {
            'location': location,
            'settings': settings,
            'supply_kit': supply_kit,
            'important_links': important_links,
            'data_bounds': data_bounds,
            'data': OrderedDict(sorted(data.items(), key=lambda t: ShapefileGroup.objects.get(name=t[0]).order_of_appearance ))
        })


    # if not, we'll still serve up the same template without data
    else:
        return render(request, 'index.html', {
            'location': location,
            'settings': settings,
            'data_bounds': data_bounds
            })
