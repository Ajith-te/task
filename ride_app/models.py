from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Ride(models.Model):
    """
    Model representing a ride request in the system.

    Attributes:
        rider (User): The user who requested the ride.
        driver (User, optional): The driver assigned to the ride.
        pickup_location (str): The starting point of the ride.
        drop_location (str): The destination of the ride.
        current_location (str, optional): The current location of the ride (updated dynamically).
        status (str): The current status of the ride. Choices: requested, ongoing, completed, cancelled.
        created_at (datetime): The timestamp when the ride was created.
        updated_at (datetime): The timestamp of the last update.
    """
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drives', null=True, blank=True)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255, blank=True, null=True)  # ✅ Merged correctly
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(default=now, editable=False)  # Change here
    updated_at = models.DateTimeField(auto_now=True)


class DriverProfile(models.Model):
    """
    Model representing a driver's profile.

    Attributes:
        user (User): The user associated with this driver profile.
        is_available (bool): Indicates whether the driver is available for new rides.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
