from django.contrib import admin

# Register your models here.

from .models import Extraction, Stock


@admin.register(Extraction)
class ExtractionAdmin(admin.ModelAdmin):
    list_display = ('site', 'extraction_date', 'quantity_tonnes', 'status', 'operator')
    list_filter = ('status', 'site')
    search_fields = ('site__name', 'notes')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('site', 'quantity_in_stock', 'last_updated')
    list_filter = ('site',)
