from rest_framework import serializers
from .models import Region, Subdivision, Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'number', 'driving_style', 'all_fines', 'all_telematics_mileage']

class SubdivisionSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = Subdivision
        fields = ['id', 'name', 'vehicles']

class RegionSerializer(serializers.ModelSerializer):
    subdivisions = SubdivisionSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'code', 'name', 'subdivisions']
