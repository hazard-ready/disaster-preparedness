from collections import OrderedDict
from .models import Snugget, SiteSettings, Location, ShapefileGroup, PastEventsPhoto, DataOverviewImage, UserProfile, SlideshowSnugget, PreparednessAction, SurveyCode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods

import logging
import json

# Remove this method when the survey is over
@csrf_exempt
@require_http_methods(["POST"])
def add_survey_code(request):
    response = HttpResponse(status=403)
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            code = body['code']
            if code is not None:
                SurveyCode.objects.create(code=code)
                response.set_cookie('survey', code)
                response.status_code = 201
            else:
                response.status_code = 400
        except ValueError:
            response.status_code = 400

    return response


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
        except ValueError as error:
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
def about_view(request):
    renderData = {
    'settings': SiteSettings.get_solo()
    }
    return render(request, "about.html", renderData)

@ensure_csrf_cookie
def data_view(request):
    renderData = {
    'settings': SiteSettings.get_solo()
    }
    return render(request, "data.html", renderData)


@ensure_csrf_cookie
def prepare_view(request):
    renderData = {
        'settings': SiteSettings.get_solo(),
        'actions': PreparednessAction.objects.all().order_by('cost'),
        'logged_in': False
    }

    if request.user.is_authenticated:
        renderData['logged_in'] = True
        renderData['actions_taken'] = UserProfile.objects.get(user=request.user).actions_taken.all().values_list('id', flat=True)

    return render(request, "prepare.html", renderData)

@ensure_csrf_cookie
def prepare_action_update(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            action_id = request.POST.get('action', '')
            action = PreparednessAction.objects.get(id=action_id)
            taken = request.POST.get('taken', '')

            if taken == 'true':
                profile.actions_taken.add(action)
            else:
                profile.actions_taken.remove(action)

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
    path = request.path[:-3] # slice off the old language code

    #Remove this when the survey is over
    showSurveyButton = False
    if 'survey' in request.COOKIES:
        showSurveyButton = True

    if 'QUERY_STRING' in request.META:
        path = path + '?' + request.META['QUERY_STRING']

    if request.user.is_authenticated:
        username = request.user.username
        profile = UserProfile.objects.get(user=request.user)


    renderData = {
        'settings': SiteSettings.get_solo(),
        'data_bounds': Location.get_data_bounds(),
        'quick_data_overview': DataOverviewImage.objects.all(),
        'username': username,
        'profile': profile,
        'nextPath': path,
        'surveyHeader': showSurveyButton
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
            data = {el:{'collapsible': {}, 'static': {}} for el in snugget_content}

            if snugget_content is not None:
                for group, snuggets in snugget_content.items():

                    if snuggets:
                        template = 'found_content.html'

                        for snugget in snuggets:
                            if snugget.percentage is not None:
                                group.percentage = snugget.percentage
                            if snugget.__class__ == SlideshowSnugget:
                                snugget.photos = PastEventsPhoto.objects.filter(snugget=snugget)

                            if snugget.section.collapsible:
                                if not snugget.section in data[group]['collapsible']:
                                    data[group]['collapsible'][snugget.section] = [snugget]
                                else:
                                    data[group]['collapsible'][snugget.section].append(snugget)
                            else:
                                if not snugget.section in data[group]['static']:
                                    data[group]['static'][snugget.section] = [snugget]
                                else:
                                    data[group]['static'][snugget.section].append(snugget)

                    # Sort the sections by order_of_appearance
                    # python 3.5 does not guarantee the ORDER of keys coming out of an ORDERED DICTIONARY.
                    data = OrderedDict(sorted(data.items(), key=lambda t: t[0].order_of_appearance))
                    data[group]['collapsible'] = OrderedDict(sorted(data[group]['collapsible'].items(), key=lambda t: t[0].order_of_appearance))
                    data[group]['static'] = OrderedDict(sorted(data[group]['static'].items(), key=lambda t: t[0].order_of_appearance))

            renderData['data'] = data

    return render(request, template, renderData)
