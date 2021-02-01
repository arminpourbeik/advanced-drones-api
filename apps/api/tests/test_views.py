from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from rest_framework_simplejwt.tokens import RefreshToken

from apps.drones.models import DroneCategory, Pilot
from apps.authentication.models import User
from .test_setup import TestSetup


class DroneCategoryTests(TestSetup):
    def post_drone_category(self, name):
        data = {"name": name}
        response = self.client.post(self.drone_category_list_url, data, format="json")
        return response

    def test_post_and_get_drone_category(self):
        """
        Ensure we can create a new Drone Category and then retrieve it
        """
        new_drone_category_name = "Hexacopter"
        response = self.post_drone_category(new_drone_category_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DroneCategory.objects.count(), 1)
        self.assertEqual(DroneCategory.objects.get().name, new_drone_category_name)

    def test_post_existing_drone_category(self):
        """
        Ensure we cannot create a new Drone Category with an existing name
        """
        new_drone_category_name = "Duplicated Copter"
        response1 = self.post_drone_category(new_drone_category_name)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.post_drone_category(new_drone_category_name)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_drone_category_by_name(self):
        """
        Ensure we can filter a drone category by name
        """
        drone_category_name1 = "Hexacopter"
        self.post_drone_category(drone_category_name1)
        drone_category_name2 = "Octocopter"
        self.post_drone_category(drone_category_name2)
        filter_by_name = {"name": drone_category_name1}
        url = "{base}?{queryparamter}".format(
            base=self.drone_category_list_url, queryparamter=urlencode(filter_by_name)
        )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure we receive only one element in the response
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], drone_category_name1)

    def test_drone_categories_collection(self):
        new_drone_category_name = "Super Copter"
        self.post_drone_category(new_drone_category_name)
        response = self.client.get(self.drone_category_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Make sure we can receive only one element in the response
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], new_drone_category_name)

    def test_update_drone_category(self):
        """
        Ensure we can update a single field for a drone category
        """

        drone_category_name = "Category initial name"
        response = self.post_drone_category(drone_category_name)
        url = reverse("dronecategory-detail", None, {response.data.get("pk")})
        print(url)
        updated_drone_category_name = "Updated Name"
        data = {"name": updated_drone_category_name}
        patch_response = self.client.patch(url, data, format="json")
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["name"], updated_drone_category_name)

    def test_get_drone_category(self):
        """
        Ensure we can get a single drone category by uuid
        """

        drone_category_name = "Easy to retrieve"
        response = self.post_drone_category(drone_category_name)
        url = reverse("dronecategory-detail", None, {response.data.get("pk")})
        get_response = self.client.get(url, format="json")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["name"], drone_category_name)


class PilotTests(TestSetup):
    def post_pilot(self, name, gender, races_count):
        """Send requirement data for creating a pilot instance"""
        url = reverse("pilot-list")
        data = {
            "name": name,
            "gender": gender,
            "races_count": races_count,
        }
        response = self.client.post(url, data, format="json")

        return response

    def create_user_and_set_token_credentials(self):
        """Create a user and set the access token in header"""
        user = User.objects.create_user(**self.user_data)
        access_token = user.tokens.get("access")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(access_token))

    def test_post_and_get_pilot(self):
        """
        Ensure we can create a new pilot and the retrieve it
        Ensure we cannot retrieve the persisted pilot without a token
        """
        self.create_user_and_set_token_credentials()
        new_pilot_name = "Gatson"
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 5
        response = self.post_pilot(
            new_pilot_name,
            new_pilot_gender,
            new_pilot_races_count,
        )
        print("PK {0}".format(Pilot.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count() == 1
        saved_pilot = Pilot.objects.get()
        assert saved_pilot.name == new_pilot_name
        assert saved_pilot.gender == new_pilot_gender
        assert saved_pilot.races_count == new_pilot_races_count
        url = reverse("pilot-detail", None, {saved_pilot.pk})
        authorized_get_response = self.client.get(url, format="json")
        assert authorized_get_response.status_code == status.HTTP_200_OK
        print(authorized_get_response.data)
        assert authorized_get_response.data.get("name") == new_pilot_name

        # Clean up credentials
        self.client.credentials()

        unauthorized_get_response = self.client.get(url, format="json")
        assert unauthorized_get_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_to_post_without_token(self):
        new_pilot_name = "Unauthorized pilot"
        new_pilot_gender = Pilot.FEMALE
        new_pilot_races_count = 4
        response = self.post_pilot(
            new_pilot_name, new_pilot_gender, new_pilot_races_count
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Pilot.objects.count(), 0)
