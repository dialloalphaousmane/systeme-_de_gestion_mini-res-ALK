from rest_framework import serializers
from .models import EnvironmentMeasure, EnvironmentAlert, EnvironmentThreshold

class EnvironmentMeasureSerializer(serializers.ModelSerializer):
    """Serializer pour les mesures environnementales"""
    site_name = serializers.CharField(source='site.name', read_only=True)
    measurement_type_display = serializers.CharField(source='get_measurement_type_display', read_only=True)
    measured_by_name = serializers.CharField(source='measured_by.get_full_name', read_only=True)
    
    class Meta:
        model = EnvironmentMeasure
        fields = ['id', 'site', 'site_name', 'measurement_type', 'measurement_type_display',
                 'value', 'unit', 'measurement_date', 'measured_by', 'measured_by_name',
                 'location', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class EnvironmentThresholdSerializer(serializers.ModelSerializer):
    """Serializer pour les seuils environnementaux"""
    
    class Meta:
        model = EnvironmentThreshold
        fields = ['id', 'measurement_type', 'warning_threshold', 'danger_threshold',
                 'critical_threshold', 'unit', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class EnvironmentAlertSerializer(serializers.ModelSerializer):
    """Serializer pour les alertes environnementales"""
    site_name = serializers.CharField(source='site.name', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = EnvironmentAlert
        fields = ['id', 'site', 'site_name', 'measure', 'title', 'description',
                 'threshold_value', 'actual_value', 'severity', 'severity_display',
                 'status', 'status_display', 'triggered_at', 'resolved_at',
                 'assigned_to', 'assigned_to_name']
        read_only_fields = ['id', 'triggered_at']
