from rest_framework import serializers
from .models import Export, ExportDocument

class ExportDocumentSerializer(serializers.ModelSerializer):
    """Serializer pour les documents d'export"""
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = ExportDocument
        fields = ['id', 'export', 'document_type', 'document_type_display', 
                 'document_file', 'uploaded_by', 'uploaded_by_name', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ExportSerializer(serializers.ModelSerializer):
    """Serializer pour les exports"""
    transport_qr = serializers.CharField(source='transport.qr_code', read_only=True)
    site_name = serializers.CharField(source='transport.extraction.site.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = Export
        fields = ['id', 'reference_number', 'transport', 'transport_qr', 'site_name',
                 'quantity_exported', 'destination_country', 'buyer', 'unit_price',
                 'total_amount', 'status', 'status_display', 'payment_status',
                 'payment_status_display', 'export_date', 'expected_delivery',
                 'actual_delivery', 'approved_by', 'approved_by_name', 'notes',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExportDetailSerializer(ExportSerializer):
    """Serializer détaillé avec documents"""
    documents = ExportDocumentSerializer(many=True, read_only=True)
    
    class Meta(ExportSerializer.Meta):
        fields = ExportSerializer.Meta.fields + ['documents']
