from django.contrib import admin

# Register your models here.

from .models import Export, ExportDocument


@admin.register(Export)
class ExportAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'status', 'payment_status', 'destination_country', 'export_date', 'approved_by')
    list_filter = ('status', 'payment_status', 'destination_country')
    search_fields = ('reference_number', 'buyer', 'destination_country')


@admin.register(ExportDocument)
class ExportDocumentAdmin(admin.ModelAdmin):
    list_display = ('export', 'document_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('document_type',)
