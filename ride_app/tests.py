from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import DriverProfile, Ride

class RideAPITestCase(APITestCase):
    """
    Test case for Ride API endpoints.

    This test case verifies the functionality of the ride management system,
    including ride status updates, driver matching, and ride acceptance.

    Setup:
        - Creates a test rider and a test driver.
        - Generates authentication tokens for both users.
        - Creates a ride request and assigns it to the rider.
        - Creates a driver profile for driver assignment testing.

    Tests:
        - test_update_status: Ensures the ride status can be updated.
        - test_match_driver: Verifies that a driver can be matched to a ride.
        - test_accept_ride: Checks if a driver can accept a matched ride.
    """

    def setUp(self):
        """
        Sets up test data including users, authentication tokens, and a ride request.
        """
        self.user = User.objects.create_user(username='ajith', password='ajith123')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location="Kochi",
            drop_location="Trivandrum",
            status="requested"
        )

        self.driver = User.objects.create_user(username='driver', password='driver123')

        if hasattr(DriverProfile, 'driver'):
            self.driver_profile = DriverProfile.objects.create(driver=self.driver, is_available=True)
        else:
            self.driver_profile = DriverProfile.objects.create(user=self.driver, is_available=True)
        self.driver_token = str(RefreshToken.for_user(self.driver).access_token)


    def test_update_status(self):
        """
        Test updating the ride status.

        Ensures that a ride status can be updated correctly via API.
        """
        response = self.client.post(
            f"/api/rides/{self.ride.id}/update_status/", 
            {"status": "started"}
        )
        self.assertEqual(response.status_code, 200, msg=f"Response content: {response.content}")
        self.assertEqual(response.json()["message"], "Ride status updated to started")


    def test_match_driver(self):
        """
        Test ride matching with an available driver.

        Ensures that an available driver is assigned to a ride when requested.
        """
        response = self.client.post(f"/api/rides/{self.ride.id}/match_driver/")
        self.assertEqual(response.status_code, 200, msg=f"Response content: {response.content}")
        self.ride.refresh_from_db()
        self.assertIsNotNone(self.ride.driver)


    def test_accept_ride(self):
        """
        Test driver accepting the ride.

        Ensures that a driver can accept a ride that is in a 'matched' state.
        """
        self.ride.status = "matched"
        self.ride.save()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.driver_token}')

        response = self.client.post(f"/api/rides/{self.ride.id}/accept_ride/")
        self.assertEqual(response.status_code, 200, msg=f"Response content: {response.content}")
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.driver, self.driver)
        self.assertEqual(self.ride.status, "ongoing")
