from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileModelTestCase(TestCase):
  def setUp(self):
    self.testUser = User.objects.create_user(
      username="test",
      password="test"
    )

  def testUserProfileBlankFields(self):
    """The UserProfile object's fields can all be blank, except for user"""
    profile = UserProfile(user=self.testUser)
    profile.save()
    self.assertEqual(profile, UserProfile.objects.get(user=self.testUser))
