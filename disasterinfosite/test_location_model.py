from django.test import TestCase
from .models import Location

class LocationModelTestCase(TestCase):
  def setUp(self):
    Location.objects.create()

  def testObjectFormation(self):
    """The Location object is created properly as a singleton"""
    location = Location.objects.get()
    self.assertEqual(location.__unicode__(), "Location Information")
