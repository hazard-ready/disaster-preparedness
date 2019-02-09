from django.shortcuts import render
from collections import OrderedDict
from .models import Snugget, Location, SiteSettings, SupplyKit, ImportantLink, ShapefileGroup, PastEventsPhoto, DataOverviewImage, UserProfile
from .fire_dial import make_icon
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie

def create_user(request):
    if request.method == 'POST':

        try:
            user = User.objects.create_user(
                username=request.POST.get('username', ''),
                email=request.POST.get('username', ''),
                password=request.POST.get('password', '')
            )
        except IntegrityError:
            return HttpResponse(status=409, reason="That user already exists.")
        except ValueError:
            return HttpResponse(status=400)

        profile = UserProfile(
            user=user,
            address1=request.POST.get('address1', ''),
            address2=request.POST.get('address2', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            zip_code=request.POST.get('zip_code', '')
        )
        try:
            profile.save()
        except (ValueError, IntegrityError):
            return HttpResponse(status=500)

        user = authenticate(
            username=request.POST.get('username', ''),
            password=request.POST.get('password', '')
        )
        if user is None:
            return HttpResponse(status=500)

        login(request, user)

        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        login(request, user)
        # Redirect to a success page.
        return HttpResponse(status=201)
    else:
        # Show an error page
        return HttpResponse(status=403)

def update_profile(request):
    if request.method == 'POST' and request.user.is_authenticated:
        username = request.user.username
        profile = UserProfile.objects.get(user=request.user)
        profile.address1 = request.POST.get('address1', '')
        profile.address2 = request.POST.get('address2', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.zip_code = request.POST.get('zip_code', '')

        try:
            profile.save()
        except (ValueError, IntegrityError):
            return HttpResponse(status=500)

        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)

@ensure_csrf_cookie
def app_view(request):
    location = Location.get_solo()
    important_links = ImportantLink.objects.all()
    settings = SiteSettings.get_solo()
    data_bounds = Location.get_data_bounds()
    supply_kit = SupplyKit.get_solo()
    supply_kit.meals = 3 * supply_kit.days
    quick_data_overview = DataOverviewImage.objects.all()
    username = None
    profile = None
    if request.user.is_authenticated:
        username = request.user.username
        profile = UserProfile.objects.get_or_create(user=request.user)

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
                        heading = values[0].group.display_name
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
                            sections[section] = OrderedDict(sorted(sub_section_dict.items(), key=lambda t: t[0].order_of_appearance))

                        photos = []
                        for p in PastEventsPhoto.objects.filter(group=values[0].group):
                            photos.append(p)

                        data[key] = {
                            'heading': heading,
                            'sections': OrderedDict(sorted(sections.items(), key=lambda t: t[0].order_of_appearance )),
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
            'data': OrderedDict(sorted(data.items(), key=lambda t: ShapefileGroup.objects.get(name=t[0]).order_of_appearance )),
            'quick_data_overview': quick_data_overview,
            'username': username,
            'profile': profile
        })


    # if not, we'll still serve up the same template without data
    else:
        return render(request, 'index.html', {
            'location': location,
            'settings': settings,
            'data_bounds': data_bounds,
            'quick_data_overview': quick_data_overview,
            'username': username,
            'profile': profile
        })
