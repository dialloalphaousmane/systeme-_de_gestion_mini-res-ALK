from rest_framework import serializers
from .models import Truck, Transport, TransportLocation

class TruckSerializer(serializers.ModelSerializer):
    """Serializer pour les camions"""
    driver_name = serializers.CharField(source='driver.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Truck
        fields = ['id', 'registration_number', 'truck_type', 'capacity_tonnes', 
                 'owner', 'driver', 'driver_name', 'status', 'status_display', 
                 'inspection_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransportLocationSerializer(serializers.ModelSerializer):
    """Serializer pour les positions GPS"""
    
    class Meta:
        model = TransportLocation
        fields = ['id', 'transport', 'latitude', 'longitude', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class TransportSerializer(serializers.ModelSerializer):
    """Serializer pour les transports"""
    extraction_site = serializers.CharField(source='extraction.site.name', read_only=True)
    truck_info = serializers.CharField(source='truck.registration_number', read_only=True)
    driver_name = serializers.CharField(source='driver.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Transport
        fields = ['id', 'qr_code', 'extraction', 'extraction_site', 'truck', 'truck_info',
                 'departure_location', 'destination', 'departure_date', 'arrival_date',
                 'quantity_transported', 'status', 'status_display', 'driver', 'driver_name',
                 'gps_tracking', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'qr_code', 'created_at', 'updated_at']


class TransportDetailSerializer(TransportSerializer):
    """Serializer détaillé avec positions GPS"""
    locations = TransportLocationSerializer(many=True, read_only=True)
    
    class Meta(TransportSerializer.Meta):
        fields = TransportSerializer.Meta.fields + ['locations']
