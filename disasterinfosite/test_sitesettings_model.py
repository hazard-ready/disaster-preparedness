from django.test import TestCase
from .models import SiteSettings


class SiteSettingsModelTestCase(TestCase):
    def setUp(self):
        SiteSettings.objects.create(
            about_text="Some sample text",
            contact_email="foo@bar.com",
            site_url="http://www.whatever.com:4949/stuff.aspx?whatever",
            site_description="This is an example disaster website",
            area_name="The affected area"
        )

    def testObjectFormation(self):
        """The SiteSettings object is created properly as a singleton"""
        settings = SiteSettings.objects.get()
        self.assertEqual(settings.__unicode__(), "Site Settings")
