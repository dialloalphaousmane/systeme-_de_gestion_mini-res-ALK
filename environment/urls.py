from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnvironmentMeasureViewSet, EnvironmentAlertViewSet, EnvironmentThresholdViewSet

router = DefaultRouter()
router.register(r'measures', EnvironmentMeasureViewSet, basename='measure')
router.register(r'alerts', EnvironmentAlertViewSet, basename='alert')
router.register(r'thresholds', EnvironmentThresholdViewSet, basename='threshold')

app_name = 'environment'

urlpatterns = [
    path('', include(router.urls)),
]
