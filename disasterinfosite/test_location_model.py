from django.test import TestCase
from .models import Location

class LocationModelTestCase(TestCase):
  def setUp(self):
    Location.objects.create(
      area_name="Melindaville",
      community_leaders="Some information about community leaders"
    )

  def testObjectFormation(self):
    """The Location object is created properly as a singleton"""
    location = Location.objects.get()
    self.assertEqual(location.__unicode__(), "Location Information")
