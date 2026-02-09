from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DashboardMetricViewSet, ReportViewSet

app_name = 'dashboard_api'

router = DefaultRouter()
router.register(r'metrics', DashboardMetricViewSet, basename='metric')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
