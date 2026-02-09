from django.contrib import admin

# Register your models here.

from .models import EnvironmentMeasure, EnvironmentAlert, EnvironmentThreshold


@admin.register(EnvironmentMeasure)
class EnvironmentMeasureAdmin(admin.ModelAdmin):
    list_display = ('site', 'measurement_type', 'value', 'unit', 'measurement_date', 'measured_by')
    list_filter = ('measurement_type', 'site')
    search_fields = ('site__name', 'location', 'notes')


@admin.register(EnvironmentAlert)
class EnvironmentAlertAdmin(admin.ModelAdmin):
    list_display = ('site', 'title', 'severity', 'status', 'triggered_at', 'assigned_to')
    list_filter = ('severity', 'status', 'site')
    search_fields = ('title', 'description')


@admin.register(EnvironmentThreshold)
class EnvironmentThresholdAdmin(admin.ModelAdmin):
    list_display = ('measurement_type', 'warning_threshold', 'danger_threshold', 'critical_threshold', 'unit', 'updated_at')
    list_filter = ('measurement_type',)
