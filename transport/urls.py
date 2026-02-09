from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, TransportViewSet

router = DefaultRouter()
router.register(r'trucks', TruckViewSet, basename='truck')
router.register(r'transports', TransportViewSet, basename='transport')

app_name = 'transport'

urlpatterns = [
    path('', include(router.urls)),
]
