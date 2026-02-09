from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import CustomUser, UserActivityLog
from .serializers import CustomUserSerializer, UserActivityLogSerializer
from .permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from .views_dashboard import (
    AdminDashboardView, AgentDashboardView, SiteManagerDashboardView,
    DriverDashboardView, CustomsDashboardView, EnvironmentDashboardView, ViewerDashboardView
)

# Vues d'authentification personnalisées
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard:redirect')

class CustomLogoutView(LogoutView):
    next_page = 'login'

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'accounts/password_reset_form.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

class CustomUserViewSet(viewsets.ModelViewSet):
	"""ViewSet pour gérer les utilisateurs"""
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer
	permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
	search_fields = ['username', 'email', 'first_name', 'last_name']
	ordering_fields = ['created_at', 'username']
    
	def get_permissions(self):
		if self.action == 'create':
			# Tout le monde peut créer un compte (inscription)
			return [AllowAny()]
		if self.action in ['update', 'partial_update', 'destroy']:
			# Seul le propriétaire du compte ou un admin peut modifier/supprimer
			return [IsAuthenticated(), IsOwnerOrAdmin()]
		return super().get_permissions()
    
	@action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
	def me(self, request):
		"""Récupérer les informations de l'utilisateur actuel"""
		serializer = self.get_serializer(request.user)
		return Response(serializer.data)
    
	@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
	def set_password(self, request, pk=None):
		"""Changer le mot de passe d'un utilisateur"""
		user = self.get_object()
		serializer = CustomUserSerializer(user, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response({'detail': 'Mot de passe changé avec succès'}, 
						  status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
	"""ViewSet pour consulter les logs d'activité"""
	queryset = UserActivityLog.objects.all()
	serializer_class = UserActivityLogSerializer
	permission_classes = [IsAuthenticated]
	ordering_fields = ['timestamp']
    
	def get_queryset(self):
		"""Filtrer par utilisateur si demandé"""
		user_id = self.request.query_params.get('user_id')
		queryset = super().get_queryset()
		if user_id:
			queryset = queryset.filter(user_id=user_id)
		return queryset
