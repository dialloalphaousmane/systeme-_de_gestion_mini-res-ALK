"""
URL configuration for SGM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from dashboard.views import HomeView, ContactFormView, CustomLoginView, dashboard_redirect_view
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Page d'accueil et formulaire de contact
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    re_path(r'^contact/`$', RedirectView.as_view(url='/contact/', permanent=False)),
    
    # Redirection de l'URL racine vers la page d'accueil
    path('home/', RedirectView.as_view(url='/', permanent=True)),
    
    # Authentification
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', dashboard_redirect_view, name='dashboard_redirect'),
    path('dashboard/', include('dashboard.web_urls', namespace='dashboard')),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints for each app
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/sites/', include('sites.urls', namespace='sites')),
    path('api/extraction/', include('extraction.urls', namespace='extraction')),
    path('api/transport/', include('transport.urls', namespace='transport')),
    path('api/export/', include('export.urls', namespace='export')),
    path('api/environment/', include('environment.urls', namespace='environment')),
    path('api/notifications/', include('notifications.urls', namespace='notifications')),
    path('api/dashboard/', include('dashboard.api_urls', namespace='dashboard_api')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

