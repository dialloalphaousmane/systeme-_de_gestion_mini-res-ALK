from django.contrib import admin

# Register your models here.

from .models import Truck, Transport, TransportLocation


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'truck_type', 'capacity_tonnes', 'status', 'driver')
    list_filter = ('status',)
    search_fields = ('registration_number', 'owner')


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('qr_code', 'status', 'departure_location', 'destination', 'driver', 'departure_date')
    list_filter = ('status',)
    search_fields = ('qr_code', 'departure_location', 'destination')


@admin.register(TransportLocation)
class TransportLocationAdmin(admin.ModelAdmin):
    list_display = ('transport', 'latitude', 'longitude', 'timestamp')
    list_filter = ('transport',)
