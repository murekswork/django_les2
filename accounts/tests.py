from django.test import TestCase
from .models import User, CustomUserManager
from django.urls import reverse

class UserModelTest(TestCase):

    def setUp(self):
        User.objects.create(username='123', is_active=False, staff=True, admin=True)

    def test_user_username(self):
        user = User.objects.get(id=1)
        expected_username = f'{user.username}'
        self.assertEqual(expected_username, '123')

    def test_user_admin(self):
        user = User.objects.get(id=1)
        expected_admin = user.is_admin()
        self.assertEqual(expected_admin, True)

    def test_user_staff(self):
        user = User.objects.get(id=1)
        expected_staff = user.is_staff()
        self.assertEqual(expected_staff, True)

class ViewsTest(TestCase):

    def test_view_url_exists_at_proper_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)


    def test_view_url_by_name(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual
# Create your tests here.
