from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ride model.

    This serializer converts Ride model instances into JSON representations 
    and handles validation and creation of Ride objects.

    Meta:
        model (Ride): The Ride model being serialized.
        fields (str): Specifies that all fields of the Ride model should be included.

    Methods:
        create(validated_data): Overrides the default create method to set the rider 
        to the authenticated user making the request.
    """
    class Meta:
        model = Ride
        fields = '__all__'


    def create(self, validated_data):
        """
        Custom create method to assign the authenticated user as the rider.

        Args:
            validated_data (dict): The validated data for creating a Ride instance.

        Returns:
            Ride: A newly created Ride instance with the authenticated user as the rider.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['rider'] = request.user
        return super().create(validated_data)


