from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count

from extraction.models import Extraction, Stock
from transport.models import Transport
from export.models import Export
from accounts.models import CustomUser
from sites.models import Site
from environment.models import EnvironmentMeasure, EnvironmentAlert


class RoleBasedDashboardMixin(LoginRequiredMixin):
    """Mixin pour s'assurer que l'utilisateur a le bon rôle pour accéder au dashboard."""
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        # Les administrateurs peuvent accéder à tous les tableaux de bord
        if request.user.role == CustomUser.Role.ADMIN:
            return super().dispatch(request, *args, **kwargs)
        
        if self.required_role and request.user.role != self.required_role:
            messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
            return redirect('dashboard_redirect')
        return super().dispatch(request, *args, **kwargs)


class AdminDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/admin/dashboard.html'
    required_role = CustomUser.Role.ADMIN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Administrateur'
        context['total_users'] = CustomUser.objects.count()
        context['active_users'] = CustomUser.objects.filter(is_active=True).count()
        context['extractions_count'] = Extraction.objects.count()
        context['transports_count'] = Transport.objects.count()
        context['exports_count'] = Export.objects.count()
        context['total_sites'] = Site.objects.count()
        context['environment_measures_count'] = EnvironmentMeasure.objects.count()
        context['active_environment_alerts'] = EnvironmentAlert.objects.filter(status='active').count()
        context['users_by_role'] = CustomUser.objects.values('role').annotate(count=Count('id')).order_by('-count')
        context['recent_users'] = CustomUser.objects.order_by('-date_joined')[:10]
        return context


class AgentDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/agent/dashboard.html'
    required_role = CustomUser.Role.AGENT_MINIER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Agent Minier'
        user = self.request.user
        context['my_extractions'] = Extraction.objects.filter(operator=user).count()
        context['pending_extractions'] = Extraction.objects.filter(operator=user, status='planifiee').count()
        context['recent_extractions'] = Extraction.objects.filter(operator=user).order_by('-extraction_date')[:10]
        context['transports_count'] = Transport.objects.count()
        context['exports_count'] = Export.objects.count()
        return context


class SiteManagerDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/site_manager/dashboard.html'
    required_role = CustomUser.Role.RESPONSABLE_SITE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Responsable de Site'
        user = self.request.user
        site = Site.objects.filter(manager=user).first()
        context['site'] = site
        if not site:
            messages.warning(self.request, "Vous n'êtes assigné à aucun site.")
            context['total_extraction_volume'] = 0
            context['current_stock'] = 0
            context['recent_transports'] = []
            return context

        context['total_extraction_volume'] = Extraction.objects.filter(site=site).aggregate(total=Sum('quantity_tonnes'))['total'] or 0
        stock = Stock.objects.filter(site=site).first()
        context['current_stock'] = getattr(stock, 'quantity_in_stock', 0) or 0
        context['recent_transports'] = Transport.objects.filter(extraction__site=site).order_by('-departure_date')[:10]
        context['transports_count'] = Transport.objects.count()
        context['exports_count'] = Export.objects.count()
        return context


class DriverDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/driver/dashboard.html'
    required_role = CustomUser.Role.CHAUFFEUR

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Chauffeur'
        user = self.request.user
        context['assigned_transports'] = Transport.objects.filter(driver=user).order_by('-departure_date')
        context['extractions_count'] = Extraction.objects.count()
        context['exports_count'] = Export.objects.count()
        return context


class CustomsDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/customs/dashboard.html'
    required_role = CustomUser.Role.DOUANE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Douane'
        context['exports_count'] = Export.objects.count()
        context['pending_exports'] = Export.objects.filter(status='en_attente').count()
        context['approved_exports'] = Export.objects.filter(status='approuvee').count()
        context['recent_exports'] = Export.objects.order_by('-export_date')[:10]
        return context


class EnvironmentDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/environment/dashboard.html'
    required_role = CustomUser.Role.ENVIRONNEMENT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Environnement'
        context['sites_count'] = Site.objects.count()
        context['extractions_count'] = Extraction.objects.count()
        context['transports_count'] = Transport.objects.count()
        return context


class ViewerDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/viewer/dashboard.html'
    # Pas de rôle requis spécifique, accessible à tout utilisateur connecté

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Visiteur'
        context['extractions_count'] = Extraction.objects.count()
        context['transports_count'] = Transport.objects.count()
        context['exports_count'] = Export.objects.count()
        return context
