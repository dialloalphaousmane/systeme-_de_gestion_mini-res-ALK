from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExtractionViewSet, StockViewSet

router = DefaultRouter()
router.register(r'extractions', ExtractionViewSet, basename='extraction')
router.register(r'stocks', StockViewSet, basename='stock')

app_name = 'extraction'

urlpatterns = [
    path('', include(router.urls)),
]
