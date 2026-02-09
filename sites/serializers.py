from rest_framework import serializers
from .models import Site, SiteOperationHistory

class SiteSerializer(serializers.ModelSerializer):
    """Serializer pour les sites miniers"""
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    mineral_type_display = serializers.CharField(source='get_mineral_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Site
        fields = ['id', 'name', 'mineral_type', 'mineral_type_display', 'latitude', 
                 'longitude', 'address', 'region', 'manager', 'manager_name', 
                 'status', 'status_display', 'capacity', 'operational_since', 
                 'license_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SiteOperationHistorySerializer(serializers.ModelSerializer):
    """Serializer pour l'historique des opérations"""
    site_name = serializers.CharField(source='site.name', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.get_full_name', read_only=True)
    
    class Meta:
        model = SiteOperationHistory
        fields = ['id', 'site', 'site_name', 'description', 'recorded_by', 
                 'recorded_by_name', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class SiteDetailSerializer(SiteSerializer):
    """Serializer détaillé incluant l'historique"""
    operation_history = SiteOperationHistorySerializer(many=True, read_only=True)
    
    class Meta(SiteSerializer.Meta):
        fields = SiteSerializer.Meta.fields + ['operation_history']
