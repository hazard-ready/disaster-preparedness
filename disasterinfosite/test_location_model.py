from django.test import TestCase
from .models import Location

class LocationModelTestCase(TestCase):
  def setUp(self):
    Location.objects.create(
      area_name="Melindaville",
      disaster_name="a zombie attack",
      disaster_description="Zombies are real, you know.",
      evacuation_routes_link="http://default.com",
      emergency_management_link="http://www.fema.gov"
    )

  def testObjectFormation(self):
    """The Location object is created properly as a singleton"""
    location = Location.objects.get()
    self.assertEqual(location.__unicode__(), "Location Information")
