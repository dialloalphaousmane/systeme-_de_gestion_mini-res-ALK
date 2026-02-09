from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, EmailNotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'emails', EmailNotificationViewSet, basename='email')

app_name = 'notifications'

urlpatterns = [
    path('', include(router.urls)),
]
