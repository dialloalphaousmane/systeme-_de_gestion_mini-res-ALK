from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', include('dashboard.api_urls')),
    path('', include('dashboard.web_urls')),
]
