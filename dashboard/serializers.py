from rest_framework import serializers
from .models import DashboardMetric, Report

class DashboardMetricSerializer(serializers.ModelSerializer):
    """Serializer pour les métriques du dashboard"""
    metric_type_display = serializers.CharField(source='get_metric_type_display', read_only=True)
    
    class Meta:
        model = DashboardMetric
        fields = ['id', 'metric_type', 'metric_type_display', 'value',
                 'period_start', 'period_end', 'calculated_at']
        read_only_fields = ['id', 'calculated_at']


class ReportSerializer(serializers.ModelSerializer):
    """Serializer pour les rapports"""
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    format_display = serializers.CharField(source='get_format_display', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Report
        fields = ['id', 'title', 'report_type', 'report_type_display', 'format',
                 'format_display', 'start_date', 'end_date', 'generated_by',
                 'generated_by_name', 'file_path', 'generated_at']
        read_only_fields = ['id', 'generated_at']
