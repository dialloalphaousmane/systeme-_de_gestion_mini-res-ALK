from django.urls import path
from .views_dashboard import (
    AdminDashboardView,
    AgentDashboardView,
    SiteManagerDashboardView,
    DriverDashboardView,
    CustomsDashboardView,
    EnvironmentDashboardView,
    ViewerDashboardView
)

app_name = 'dashboard'

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('agent/', AgentDashboardView.as_view(), name='agent_dashboard'),
    path('site-manager/', SiteManagerDashboardView.as_view(), name='site_manager_dashboard'),
    path('driver/', DriverDashboardView.as_view(), name='driver_dashboard'),
    path('customs/', CustomsDashboardView.as_view(), name='customs_dashboard'),
    path('environment/', EnvironmentDashboardView.as_view(), name='environment_dashboard'),
    path('viewer/', ViewerDashboardView.as_view(), name='viewer_dashboard'),
]
