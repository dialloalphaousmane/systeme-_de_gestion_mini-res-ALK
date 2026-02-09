from rest_framework import serializers
from .models import Extraction, Stock

class ExtractionSerializer(serializers.ModelSerializer):
    """Serializer pour les extractions"""
    site_name = serializers.CharField(source='site.name', read_only=True)
    operator_name = serializers.CharField(source='operator.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Extraction
        fields = ['id', 'site', 'site_name', 'extraction_date', 'quantity_tonnes', 
                 'quality_grade', 'operator', 'operator_name', 'status', 'status_display', 
                 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    """Serializer pour les stocks"""
    site_name = serializers.CharField(source='site.name', read_only=True)
    site_mineral_type = serializers.CharField(source='site.get_mineral_type_display', read_only=True)
    
    class Meta:
        model = Stock
        fields = ['id', 'site', 'site_name', 'site_mineral_type', 'quantity_in_stock', 'last_updated']
        read_only_fields = ['id', 'last_updated']
