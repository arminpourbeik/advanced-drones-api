from rest_framework import status
from django.urls import reverse
from django.utils.http import urlencode

from apps.drones.models import DroneCategory, Pilot
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
        Ensure we can get a single drone category by id
        """

        drone_category_name = "Easy to retrieve"
        response = self.post_drone_category(drone_category_name)
        url = reverse("dronecategory-detail", None, {response.data.get("pk")})
        get_response = self.client.get(url, format="json")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["name"], drone_category_name)
