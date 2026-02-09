from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from .forms import ContactForm
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import DashboardMetric, Report
from .serializers import DashboardMetricSerializer, ReportSerializer
from extraction.models import Extraction, Stock
from transport.models import Transport, Truck
from accounts.models import CustomUser
from sites.models import Site

# Vue pour la page d'accueil
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Accueil - SGM'
        context['contact_form'] = ContactForm()
        return context

class DashboardMetricViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = DashboardMetric.objects.all()
	serializer_class = DashboardMetricSerializer
	permission_classes = [IsAuthenticated]
	ordering_fields = ['calculated_at']
    
	@action(detail=False, methods=['get'])
	def summary(self, request):
		from sites.models import Site
		from django.utils import timezone
		summary = {
			'total_sites': Site.objects.filter(status='actif').count(),
			'total_extractions': Extraction.objects.count(),
			'total_extraction_volume': Extraction.objects.aggregate(total=Sum('quantity_tonnes'))['total'] or 0,
			'active_transports': Transport.objects.filter(status='en_transit').count(),
			'total_exports': Export.objects.count(),
			'export_revenue': Export.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
		}
		return Response(summary)


class ContactFormView(FormView):
    template_name = 'home.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        try:
            form.send_email()
            messages.success(self.request, 'Votre message a été envoyé avec succès. Nous vous répondrons dès que possible.')
        except Exception as e:
            messages.error(self.request, f"Une erreur s'est produite lors de l'envoi du message: {str(e)}")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return f"{super().get_success_url()}#contact"


def dashboard_redirect_view(request):
    """Redirige l'utilisateur vers le tableau de bord approprié en fonction de son rôle"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer le rôle de l'utilisateur
    role = getattr(request.user, 'role', None)
    
    # Mapper les rôles aux URLs des tableaux de bord
    dashboard_urls = {
        'admin': 'dashboard:admin_dashboard',
        'agent_minier': 'dashboard:agent_dashboard',
        'responsable_site': 'dashboard:site_manager_dashboard',
        'chauffeur': 'dashboard:driver_dashboard',
        'douane': 'dashboard:customs_dashboard',
        'environnement': 'dashboard:environment_dashboard',
    }
    
    # URL par défaut pour les rôles non spécifiés ou les visiteurs
    default_url = 'dashboard:viewer_dashboard'
    
    # Rediriger vers le tableau de bord approprié
    return redirect(dashboard_urls.get(role, default_url))


class ReportViewSet(viewsets.ModelViewSet):
	queryset = Report.objects.all()
	serializer_class = ReportSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['title', 'report_type']
	ordering_fields = ['generated_at']
    
	def perform_create(self, serializer):
		serializer.save(generated_by=self.request.user)
    
	@action(detail=False, methods=['post'])
	def generate_extraction_report(self, request):
		start_date = request.data.get('start_date')
		end_date = request.data.get('end_date')
		report_format = request.data.get('format', 'pdf')
		report = Report.objects.create(
			title=f"Rapport d'extraction {start_date} à {end_date}",
			report_type='extraction_summary',
			format=report_format,
			start_date=start_date,
			end_date=end_date,
			generated_by=request.user
		)
		serializer = self.get_serializer(report)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(detail=False, methods=['post'])
	def generate_export_report(self, request):
		start_date = request.data.get('start_date')
		end_date = request.data.get('end_date')
		report_format = request.data.get('format', 'pdf')
		report = Report.objects.create(
			title=f"Rapport d'export {start_date} à {end_date}",
			report_type='export_analysis',
			format=report_format,
			start_date=start_date,
			end_date=end_date,
			generated_by=request.user
		)
		serializer = self.get_serializer(report)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard_redirect')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'Bienvenue {form.get_user().username}! Vous êtes maintenant connecté.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Nom d\'utilisateur ou mot de passe incorrect. Veuillez réessayer.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse('dashboard_redirect')


class RoleBasedDashboardMixin(LoginRequiredMixin):
    """Mixin pour s'assurer que l'utilisateur a le bon rôle pour accéder au dashboard."""
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.required_role and request.user.role != self.required_role:
            messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
            return redirect('dashboard_redirect')
        return super().dispatch(request, *args, **kwargs)

class AdminDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/admin.html'
    required_role = CustomUser.Role.ADMIN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Administrateur'
        context['total_users'] = CustomUser.objects.count()
        context['total_extractions'] = Extraction.objects.count()
        context['total_transports'] = Transport.objects.count()
        context['total_sites'] = Site.objects.count()
        context['recent_users'] = CustomUser.objects.order_by('-date_joined')[:5]
        return context

# Vues pour les autres rôles (à implémenter)
class AgentDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/agent.html'
    required_role = CustomUser.Role.AGENT_MINIER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Agent Minier'
        user = self.request.user

        # Récupérer les extractions assignées à l'agent
        context['my_extractions'] = Extraction.objects.filter(operator=user).order_by('-extraction_date')[:10]

        # Récupérer les informations du site (suppose que l'agent est lié à un site principal)
        # Note: Cette logique peut nécessiter un ajustement si un agent peut travailler sur plusieurs sites.
        site = Site.objects.filter(extractions__operator=user).first()
        if site:
            context['site'] = site
            context['site_stock'] = Stock.objects.filter(site=site).first()

        return context

class SiteManagerDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/site_manager.html'
    required_role = CustomUser.Role.RESPONSABLE_SITE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tableau de Bord Responsable Site'
        user = self.request.user

        # Trouver le site géré par cet utilisateur
        # Hypothèse : un responsable est lié à un site. À adapter si plusieurs sites.
        site = Site.objects.filter(extractions__operator=user).distinct().first()
        context['site'] = site

        if site:
            # Statistiques du site
            context['site_extractions'] = Extraction.objects.filter(site=site)
            context['total_extraction_volume'] = context['site_extractions'].aggregate(total=Sum('quantity_tonnes'))['total'] or 0
            context['site_stock'] = Stock.objects.filter(site=site).first()
            context['recent_transports'] = Transport.objects.filter(extraction__site=site).order_by('-departure_date')[:5]

        return context

class DriverDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/driver.html'
    required_role = CustomUser.Role.CHAUFFEUR
    # ... la logique de la vue sera ajoutée ici

class CustomsDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/customs.html'
    required_role = CustomUser.Role.DOUANE
    # ... la logique de la vue sera ajoutée ici

class EnvironmentDashboardView(RoleBasedDashboardMixin, TemplateView):
    template_name = 'dashboard/environment.html'
    required_role = CustomUser.Role.ENVIRONNEMENT
    # ... la logique de la vue sera ajoutée ici

class ViewerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/viewer.html'
    # ... la logique de la vue sera ajoutée ici
