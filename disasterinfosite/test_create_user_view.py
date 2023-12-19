from django.test import TestCase
from django.test.client import RequestFactory
from .views import create_user
from .models import UserProfile
from django.http import HttpResponse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
import unittest
from unittest.mock import patch
import logging

request_url = '/accounts/create_user/'

logger = logging.getLogger(__name__)

class CreateUserViewTestCase(TestCase):
    def makeRequest(self, body):
        request = self.request_factory.post(request_url, body)
        middleware = SessionMiddleware(request)
        middleware.process_request(request)
        request.session.save()
        return request

    def setUp(self):
        self.request_factory = RequestFactory()

    def testOnlyPostAccepted(self):
        """ This REST endpoint only accepts POST requests. """
        request_body = {}
        request = self.makeRequest(request_body)
        disallowed_methods = ["GET", "HEAD", "PUT",
                              "DELETE", "OPTIONS", "TRACE", "CONNECT", "ASDF"]
        for method in disallowed_methods:
            request.method = method
            self.assertEqual(405, create_user(request).status_code)

    def testDuplicateUserError(self):
        """ Errors arising from creating a duplicate user are handled """
        request_body = {
            "username": "test_duplicates",
            "email": "test",
            "password": "test",
            "address1": "",
            "address2": "",
            "city": "",
            "state": "",
            "zip_code": ""
        }
        create_user(self.makeRequest(request_body))
        self.assertEqual(409, create_user(
            self.makeRequest(request_body)).status_code
        )

    def testUserCreationFails(self):
        """ It handles the case when creating a new user fails """
        request_body = {
            "invalid_field": "foo"
        }
        request = self.makeRequest(request_body)
        self.assertEqual(400, create_user(request).status_code)

    @patch.object(UserProfile, "save", side_effect=ValueError())
    def testProfileSaveFails(self, mock_profile):
        """ It returns a 500 and an error message when saving the newly created profile fails """
        request_body = {
            "username": "test_profile_save",
            "email": "test",
            "password": "test",
            "invalid_field": "foo"
        }
        request = self.makeRequest(request_body)
        self.assertEqual(500, create_user(request).status_code)

    def testProfileCreated(self):
        """ A profile for the user is created. """
        request_body = {
            "username": "test_profile",
            "email": "test",
            "password": "test",
            "address1": "test address1",
            "address2": "test address2",
            "city": "test city",
            "state": "test state",
            "zip_code": "test zip"
        }
        create_user(self.makeRequest(request_body))
        user = User.objects.get(username=request_body['username'])
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.address1, request_body['address1'])
        self.assertEqual(profile.state, request_body['state'])
        self.assertEqual(profile.address2, request_body['address2'])
        self.assertEqual(profile.city, request_body['city'])
        self.assertEqual(profile.zip_code, request_body['zip_code'])

    def testUserLoggedIn(self):
        """ After the user and profile are created, the user is logged in """
        request_body = {
            "username": "test_logged_in",
            "email": "test",
            "password": "test",
            "address1": "test address1",
            "address2": "test address2",
            "city": "test city",
            "state": "test state",
            "zip_code": "test zip"
        }
        create_user(self.makeRequest(request_body))
        user = User.objects.get(username=request_body['username'])
        self.assertTrue(user.is_authenticated)

    def test201OnSuccess(self):
        """ If a user is successfully created, it returns a 201. """
        request_body = {
            "username": "test_happy_path",
            "email": "test",
            "password": "test",
            "address1": "test address1",
            "address2": "test address2",
            "city": "test city",
            "state": "test state",
            "zip_code": "test zip"
        }
        self.assertTrue(201, create_user(
            self.makeRequest(request_body)).status_code)
