from rest_framework import serializers
from .models import Region, Subdivision, Vehicle, Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"

class VehicleSerializer(serializers.ModelSerializer):
    trips = TripSerializer(many=True, read_only=True)
    class Meta:
        model = Vehicle
        fields = ['id', 'number', 'driving_style', 'all_fines', 'all_telematics_mileage', 'in_structure', 'trips']

class SubdivisionSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = Subdivision
        fields = ['id', 'name', 'vehicles_count', 'vehicles']

class RegionSerializer(serializers.ModelSerializer):
    subdivisions = SubdivisionSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'code', 'name', 'vehicles_count', 'subdivisions']
