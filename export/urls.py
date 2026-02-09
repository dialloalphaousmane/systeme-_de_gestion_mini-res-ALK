from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExportViewSet, ExportDocumentViewSet

router = DefaultRouter()
router.register(r'exports', ExportViewSet, basename='export')
router.register(r'documents', ExportDocumentViewSet, basename='document')

app_name = 'export'

urlpatterns = [
    path('', include(router.urls)),
]
