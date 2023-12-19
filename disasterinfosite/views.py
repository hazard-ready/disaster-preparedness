from collections import OrderedDict
from .models import (
    DataOverviewImage,
    Location,
    PastEventsPhoto,
    PreparednessAction,
    ShapefileGroup,
    SlideshowSnugget,
    Snugget,
    UserProfile
)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _
from django.urls import reverse

import logging
import re

logger = logging.getLogger(__name__)


def reverse_no_i18n(viewname, *args, **kwargs):
    result = reverse(viewname, *args, **kwargs)
    m = re.match(r'(/[^/]*)(/.*$)', result)
    return m.groups()[1]


@require_http_methods(["POST"])
def create_user(request):
    try:
        user = User.objects.create_user(
            username=request.POST.get('username', ''),
            email=request.POST.get('username', ''),
            password=request.POST.get('password', '')
        )
    except IntegrityError:
        return TemplateResponse(
            request,
            "registration/simple_message.html",
            {
                'message': _("That email address has already been used. Try logging in instead."),
                'error': True
            },
            status=409
        )
    except ValueError as error:
        logger.error("Unable to create a user")
        return TemplateResponse(request, "registration/simple_message.html", {
            'message': _("Whoops, we're not sure what happened there. Maybe you should try again."),
            'error': True
        }, status=400)

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
        logger.error("Unable to save a user profile")
        return TemplateResponse(request, "registration/simple_message.html", {
            'message': _("Whoops, we're not sure what happened there. Maybe you should try again."),
            'error': True
        }, status=500)

    user = authenticate(
        username=request.POST.get('username', ''),
        password=request.POST.get('password', '')
    )
    if user is None:
        logger.error("Unable to authenticate a newly created user")
        return TemplateResponse(request, "registration/simple_message.html", {
            'message': _("Whoops, we're not sure what happened there. Maybe you should try again."),
            'error': True
        }, status=500)

    login(request, user)
    return render(request, "registration/simple_message.html", {
        'message': _("Thanks for signing up! We'll get ahold of you with relevant news and information. You can come back anytime to update your address."),
        'error': True
    })


@require_http_methods(["POST"])
def update_profile(request):
    if request.user.is_authenticated:
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
            logger.error("Unable to save a user profile")
            return TemplateResponse(request, "registration/simple_message.html", {
                'message': _("Whoops, we're not sure what happened there. Maybe you should try again."),
                'error': True
            }, status=500)

        return render(request, "registration/simple_message.html", {
            'message': _("Thanks for keeping us up to date!")})

    else:
        return HttpResponse(status=403)


@ensure_csrf_cookie
def about_view(request):
    renderData = {
        'nextPath': reverse_no_i18n('about')
    }
    return render(request, "about.html", renderData)


@ensure_csrf_cookie
def data_view(request):
    renderData = {
        'nextPath': reverse_no_i18n('data'),
        'quick_data_overview': DataOverviewImage.objects.all()

    }
    return render(request, "data.html", renderData)


@ensure_csrf_cookie
def prepare_view(request):
    renderData = {
        'actions': PreparednessAction.objects.all().order_by('cost'),
        'logged_in': False,
        'nextPath': reverse_no_i18n('prepare')
    }

    if request.user.is_authenticated:
        renderData['logged_in'] = True
        renderData['actions_taken'] = UserProfile.objects.get(
            user=request.user).actions_taken.all().values_list('id', flat=True)

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
    path = reverse_no_i18n('index')

    if 'QUERY_STRING' in request.META:
        path = path + '?' + request.META['QUERY_STRING']

    if request.user.is_authenticated:
        username = request.user.username
        profile = UserProfile.objects.get(user=request.user)

    renderData = {
        'data_bounds': Location.get_data_bounds(),
        'username': username,
        'profile': profile,
        'nextPath': path

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
            snugget_content = Snugget.findSnuggetsForPoint(
                lat=float(lat), lng=float(lng))
            data = {el: {'collapsible': {}, 'static': {}}
                    for el in snugget_content}

            if snugget_content is not None:
                for group, snuggets in snugget_content.items():

                    if snuggets:
                        template = 'found_content.html'

                        for snugget in snuggets:
                            if snugget.percentage is not None:
                                group.percentage = snugget.percentage
                            if snugget.__class__ == SlideshowSnugget:
                                snugget.photos = sorted(PastEventsPhoto.objects.filter(
                                    snugget=snugget), key=lambda p: (p.image.height / p.image.width) + len(p.caption), reverse=True)

                            if snugget.section.collapsible:
                                if not snugget.section in data[group]['collapsible']:
                                    data[group]['collapsible'][snugget.section] = [
                                        snugget]
                                else:
                                    data[group]['collapsible'][snugget.section].append(
                                        snugget)
                            else:
                                if not snugget.section in data[group]['static']:
                                    data[group]['static'][snugget.section] = [
                                        snugget]
                                else:
                                    data[group]['static'][snugget.section].append(
                                        snugget)

                    # Sort the sections by order_of_appearance
                    # python 3.5 does not guarantee the ORDER of keys coming out of an ORDERED DICTIONARY.
                    data = OrderedDict(
                        sorted(data.items(), key=lambda t: t[0].order_of_appearance))
                    data[group]['collapsible'] = OrderedDict(sorted(
                        data[group]['collapsible'].items(), key=lambda t: t[0].order_of_appearance))
                    data[group]['static'] = OrderedDict(
                        sorted(data[group]['static'].items(), key=lambda t: t[0].order_of_appearance))

            renderData['data'] = data

    return render(request, template, renderData)
