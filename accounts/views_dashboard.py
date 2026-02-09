from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta

from .mixins import (
    AdminRequiredMixin, AgentMineraiRequiredMixin, SiteManagerRequiredMixin,
    DriverRequiredMixin, CustomsOfficerRequiredMixin, EnvironmentOfficerRequiredMixin,
    ViewerRequiredMixin, DashboardMixin, PermissionRequiredMixin
)
from .models import CustomUser, UserActivityLog
from .forms import CustomUserCreationForm
from extraction.models import Extraction
from transport.models import Transport
from export.models import Export


# ==================== VUES COMMUNES ====================

class DashboardBaseView(DashboardMixin, TemplateView):
    """Vue de base pour les tableaux de bord"""
    template_name = 'dashboard/base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Statistiques communes
        context['extractions_count'] = Extraction.objects.count()
        context['transports_count'] = Transport.objects.count()
        context['exports_count'] = Export.objects.count()
        
        # Dernières activités
        context['recent_activities'] = UserActivityLog.objects.filter(
            user=user
        ).order_by('-timestamp')[:5]
        
        return context


# ==================== TABLEAU DE BORD ADMINISTRATEUR ====================

class AdminDashboardView(AdminRequiredMixin, DashboardBaseView):
    """Tableau de bord de l'administrateur"""
    template_name = 'dashboard/admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques utilisateurs
        context['total_users'] = CustomUser.objects.count()
        context['active_users'] = CustomUser.objects.filter(is_active=True).count()
        context['users_by_role'] = CustomUser.objects.values('role').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Activité récente
        context['recent_users'] = CustomUser.objects.all().order_by('-date_joined')[:5]
        
        return context


# ==================== GESTION DES UTILISATEURS (ADMIN) ====================

class UserListView(AdminRequiredMixin, ListView):
    """Vue pour lister tous les utilisateurs pour l'administrateur."""
    model = CustomUser
    template_name = 'dashboard/admin/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        return CustomUser.objects.all().order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Gestion des Utilisateurs")
        return context


class UserCreateView(AdminRequiredMixin, CreateView):
    """Vue pour créer un nouvel utilisateur."""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'dashboard/admin/user_form.html'
    success_url = reverse_lazy('dashboard:admin_user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _("Créer un nouvel utilisateur")
        return context

    def form_valid(self, form):
        messages.success(self.request, _("L'utilisateur a été créé avec succès."))
        return super().form_valid(form)


# ==================== TABLEAU DE BORD AGENT MINIER ====================

class AgentDashboardView(AgentMineraiRequiredMixin, DashboardBaseView):
    """Tableau de bord de l'agent minier"""
    template_name = 'dashboard/agent/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Statistiques d'extraction
        context['my_extractions'] = Extraction.objects.filter(created_by=user).count()
        context['pending_extractions'] = Extraction.objects.filter(
            status='en_attente'
        ).count()
        
        # Dernières extractions
        context['recent_extractions'] = Extraction.objects.filter(
            created_by=user
        ).order_by('-created_at')[:5]
        
        return context


# ==================== TABLEAU DE BORD RESPONSABLE DE SITE ====================

class SiteManagerDashboardView(SiteManagerRequiredMixin, DashboardBaseView):
    """Tableau de bord du responsable de site"""
    template_name = 'dashboard/site_manager/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques du site
        context['site_extractions'] = Extraction.objects.filter(
            site__manager=self.request.user
        ).count()
        
        context['pending_approvals'] = Extraction.objects.filter(
            site__manager=self.request.user,
            status='en_attente_validation'
        ).count()
        
        # Extraire les statistiques mensuelles
        today = datetime.now()
        first_day = today.replace(day=1)
        last_month = first_day - timedelta(days=1)
        
        context['current_month_extractions'] = Extraction.objects.filter(
            site__manager=self.request.user,
            created_at__month=first_day.month,
            created_at__year=first_day.year
        ).count()
        
        context['last_month_extractions'] = Extraction.objects.filter(
            site__manager=self.request.user,
            created_at__month=last_month.month,
            created_at__year=last_month.year
        ).count()
        
        return context


# ==================== TABLEAU DE BORD CHAUFFEUR ====================

class DriverDashboardView(DriverRequiredMixin, DashboardBaseView):
    """Tableau de bord du chauffeur"""
    template_name = 'dashboard/driver/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Commandes de transport
        context['assigned_transports'] = Transport.objects.filter(
            driver=user,
            status__in=['en_attente', 'en_cours']
        ).count()
        
        context['completed_transports'] = Transport.objects.filter(
            driver=user,
            status='termine'
        ).count()
        
        # Prochains transports
        context['upcoming_transports'] = Transport.objects.filter(
            driver=user,
            scheduled_date__gte=datetime.now().date()
        ).order_by('scheduled_date')[:5]
        
        return context


# ==================== TABLEAU DE BORD DOUANE ====================

class CustomsDashboardView(CustomsOfficerRequiredMixin, DashboardBaseView):
    """Tableau de bord de l'agent des douanes"""
    template_name = 'dashboard/customs/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques des exports
        context['pending_validations'] = Export.objects.filter(
            status='en_attente_validation_douane'
        ).count()
        
        context['validated_exports'] = Export.objects.filter(
            status='valide',
            validated_by=self.request.user
        ).count()
        
        # Dernières validations
        context['recent_validations'] = Export.objects.filter(
            validated_by=self.request.user
        ).order_by('-validation_date')[:5]
        
        return context


# ==================== TABLEAU DE BORD ENVIRONNEMENT ====================

class EnvironmentDashboardView(EnvironmentOfficerRequiredMixin, DashboardBaseView):
    """Tableau de bord du responsable environnement"""
    template_name = 'dashboard/environment/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Alertes environnementales
        context['active_alerts'] = 0  # À implémenter avec le modèle d'alertes
        
        # Indicateurs environnementaux
        context['sites_monitored'] = 0  # À implémenter avec le modèle de sites
        
        return context


# ==================== TABLEAU DE BORD LECTEUR ====================

class ViewerDashboardView(ViewerRequiredMixin, DashboardBaseView):
    """Tableau de bord du lecteur/visiteur"""
    template_name = 'dashboard/viewer/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques en lecture seule
        context['total_extractions'] = Extraction.objects.count()
        context['total_transports'] = Transport.objects.count()
        context['total_exports'] = Export.objects.count()
        
        return context
