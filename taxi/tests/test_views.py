from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


class PrivateViewAccessTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="password123",
            license_number="AAA12345"
        )

    def test_unauthenticated_access_redirects(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_access_success(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")


class SearchViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="searchuser",
            password="password123",
            license_number="BBB12345"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car1 = Car.objects.create(
            model="Toyota Corolla", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Toyota Camry", manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="Ford Focus", manufacturer=self.manufacturer
        )

    def test_car_search_filter(self):
        url = reverse("taxi:car-list") + "?model=toyota"
        response = self.client.get(url)

        self.assertIn(self.car1, response.context["car_list"])
        self.assertIn(self.car2, response.context["car_list"])
        self.assertNotIn(self.car3, response.context["car_list"])
