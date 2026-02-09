from django.contrib import admin

# Register your models here.

from .models import Site, SiteOperationHistory


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'mineral_type', 'region', 'status', 'manager')
    list_filter = ('status', 'mineral_type', 'region')
    search_fields = ('name', 'license_number', 'region')


@admin.register(SiteOperationHistory)
class SiteOperationHistoryAdmin(admin.ModelAdmin):
    list_display = ('site', 'timestamp', 'recorded_by')
    list_filter = ('site',)
    search_fields = ('description',)
