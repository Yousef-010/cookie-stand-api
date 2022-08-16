from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CookieStand

###########################################################################################
# NOTE:
# The type of database that using in testing by default is sqlite3 we need to
# ensure that is to comment out all the Postgres stuff in project/.env
# DATABASES should be set to use SQLite
###########################################################################################


class CookieStandTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_cookie_stands = CookieStand.objects.create(
            location="test",
            owner=testuser1,
            description="testing",
        )
        test_cookie_stands.save()

    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_cookie_stands_model(self):
        cookie_stands = CookieStand.objects.get(id=1)
        actual_owner = str(cookie_stands.owner)
        actual_location = str(cookie_stands.location)
        actual_description = str(cookie_stands.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_location, "test")
        self.assertEqual(
            actual_description, "testing"
        )

    def test_get_cookie_stands_list(self):
        url = reverse("cookie_stands_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stands = response.data
        self.assertEqual(len(cookie_stands), 1)
        self.assertEqual(cookie_stands[0]["location"], "test")

    def test_get_cookie_stands_by_id(self):
        url = reverse("cookie_stands_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stands = response.data
        self.assertEqual(cookie_stands["location"], "test")

    def test_create_cookie_stands(self):
        url = reverse("cookie_stands_list")
        data = {"owner": 1, "location": "test2", "description": "testing2"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cookie_stands = CookieStand.objects.all()
        self.assertEqual(len(cookie_stands), 2)
        self.assertEqual(CookieStand.objects.get(id=2).location, "test2")

    def test_update_cookie_stands(self):
        url = reverse("cookie_stands_detail", args=(1,))
        data = {
            "owner": 1,
            "location": "test updated",
            "description": "testing ",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stands = CookieStand.objects.get(id=1)
        self.assertEqual(cookie_stands.location, "test updated")
        self.assertEqual(cookie_stands.owner.id, 1)
        self.assertEqual(cookie_stands.description, "testing")

    def test_delete_cookie_stands(self):
        url = reverse("cookie_stands_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cookie_stands = CookieStand.objects.all()
        self.assertEqual(len(cookie_stands), 0)

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("cookie_stands_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
