from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet, 
    UserActivityLogViewSet,
    CustomLoginView, 
    CustomLogoutView, 
    CustomPasswordResetView, 
    CustomPasswordResetDoneView, 
    CustomPasswordResetConfirmView, 
    CustomPasswordResetCompleteView
)

app_name = 'accounts'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'activity-logs', UserActivityLogViewSet, basename='activity-log')

urlpatterns = [
    # API
    path('api/', include(router.urls)),

    # Authentification
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Réinitialisation du mot de passe
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
