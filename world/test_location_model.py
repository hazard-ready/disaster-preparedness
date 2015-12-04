from django.test import TestCase
from .models import Location

class LocationModelTestCase(TestCase):
  def setUp(self):
    Location.objects.create(
      area_name="Melindaville",
      about_text="Some sample text",
      contact_email="foo@bar.com",
      site_url="http://www.whatever.com:4949/stuff.aspx?whatever",
      site_description="This is an example disaster website",
      disaster_name="a zombie attack",
      disaster_description="Zombies are real, you know."
    )

  def testObjectFormation(self):
    """The Location object is created properly as a singleton"""
    location = Location.objects.get()
    self.assertEqual(location.__unicode__(), "Location Information")
