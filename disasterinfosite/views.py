from collections import OrderedDict
from .models import Snugget, Location, SiteSettings, SupplyKit, ImportantLink, ShapefileGroup, PastEventsPhoto, DataOverviewImage, UserProfile, SlideshowSnugget
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

import logging

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

def logout_view(request):
    logout(request)
    return HttpResponse(status=201)

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

    username = None
    profile = None

    if request.user.is_authenticated:
        username = request.user.username
        profile = UserProfile.objects.get_or_create(user=request.user)


    renderData = {
        'location': Location.get_solo(),
        'settings': SiteSettings.get_solo(),
        'data_bounds': Location.get_data_bounds(),
        'quick_data_overview': DataOverviewImage.objects.all(),
        'username': username,
        'profile': profile
    }

    template = "index.html"

    # if user submitted lat/lng, find our snuggets and send them to our template
    if 'lat' and 'lng' in request.GET:
        lat = request.GET['lat']
        lng = request.GET['lng']

        if'loc' in request.GET:
            renderData['location_name'] = request.GET['loc']

        template = "no_content_found.html"

        if lat and lng:
            snugget_content = Snugget.findSnuggetsForPoint(lat=float(lat), lng=float(lng))
            data = {el:{} for el in snugget_content.keys()}

            if snugget_content is not None:
                for group, snuggets in snugget_content.items():

                    if snuggets:
                        template = 'found_content.html'

                        for snugget in snuggets:
                            if snugget.percentage:
                                group.percentage = snugget.percentage
                            if snugget.__class__ == SlideshowSnugget:
                                snugget.photos = PastEventsPhoto.objects.filter(snugget=snugget)

                            if not snugget.section in data[group]:
                                data[group][snugget.section] = [snugget]
                            else:
                                data[group][snugget.section].append(snugget)

                    # Sort the sections by order_of_appearance
                    data[group] = OrderedDict(sorted(data[group].items(), key=lambda t: t[0].order_of_appearance))

            renderData['data'] = data

    return render(request, template, renderData)
