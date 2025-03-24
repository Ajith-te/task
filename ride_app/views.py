import random
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import DriverProfile, Ride
from django.shortcuts import get_object_or_404
from .serializers import RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Ride operations.

    This ViewSet provides CRUD operations for the Ride model and 
    includes additional actions for updating ride status, matching 
    drivers, updating ride location, and accepting rides.

    Attributes:
        queryset (QuerySet): The queryset containing all Ride objects.
        serializer_class (Serializer): The serializer used for Ride instances.
        permission_classes (list): Defines the authentication requirement (IsAuthenticated).

    Methods:
        perform_create(serializer):
            Assigns the authenticated user as the rider when creating a ride.

        update_status(request, pk=None):
            Updates the status of a ride (e.g., started, completed, canceled).

        update_location(request, pk=None):
            Updates the current location of an ongoing ride.

        match_driver(request, pk=None):
            Assigns an available driver to a ride if no driver is assigned.

        accept_ride(request, pk=None):
            Allows a driver to accept a matched ride and change its status to ongoing.
    """

    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        """
        Assigns the authenticated user as the rider when creating a ride.

        Args:
            serializer (RideSerializer): The serializer instance with validated data.
        """
        serializer.save(rider=self.request.user)


    @action(detail=True, methods=['POST'])
    def update_status(self, request, pk=None):
        """
        Updates the status of a ride.

        Args:
            request (Request): The request object containing the new status.
            pk (int): The primary key of the ride.

        Returns:
            Response: A response indicating success or failure.
        """
        ride = get_object_or_404(Ride, id=pk)
        new_status = request.data.get("status")

        if new_status not in ["started", "completed", "canceled"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = new_status
        ride.save()
        return Response({"message": f"Ride status updated to {new_status}"}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['POST'], url_path='update-location')
    def update_location(self, request, pk=None):
        """
        Updates the current location of an ongoing ride.

        Args:
            request (Request): The request object containing the new location.
            pk (int): The primary key of the ride.

        Returns:
            Response: A response indicating success or failure.
        """
        try:
            ride = Ride.objects.get(id=pk, status='ongoing')
            ride.current_location = request.data.get("current_location", "Unknown Location")
            ride.save()
            return Response({"message": f"Ride is now at {ride.current_location}"}, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found or not started"}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['POST'])
    def match_driver(self, request, pk=None):
        """
        Assigns an available driver to a ride.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the ride.

        Returns:
            Response: A response indicating success or failure.
        """
        ride = get_object_or_404(Ride, id=pk)

        if ride.driver:
            return Response({"message": "Driver already assigned"}, status=status.HTTP_400_BAD_REQUEST)

        available_driver = DriverProfile.objects.filter(is_available=True).first()
        if not available_driver:
            return Response({"message": "No available drivers"}, status=status.HTTP_404_NOT_FOUND)

        ride.driver = available_driver.user
        ride.status = "matched"
        ride.save()

        return Response({"message": f"Driver {available_driver.user.username} assigned"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'])
    def accept_ride(self, request, pk=None):
        """
        Allows a driver to accept a matched ride and update its status.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the ride.

        Returns:
            Response: A response indicating success or failure.
        """
        ride = get_object_or_404(Ride, id=pk)

        if ride.status != "matched":
            return Response({"error": "Ride is not available for acceptance"}, status=status.HTTP_400_BAD_REQUEST)

        ride.driver = request.user
        ride.status = "ongoing"
        ride.save()

        return Response({"message": "Ride accepted"}, status=status.HTTP_200_OK)


