from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from faker import Faker


class TestSetup(APITestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.fake = Faker()

        self.user_data = {
            "email": self.fake.email(),
            "username": self.fake.email().split("@")[0],
            "password": "p@assw0rd",
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
