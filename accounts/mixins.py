from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class RoleRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur a un rôle spécifique"""
    required_roles = []
    permission_required = None
    login_url = 'login'
    redirect_field_name = 'next'
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
            
        if self.permission_required and not self.request.user.has_perm(self.permission_required):
            return False
            
        if not self.required_roles:
            return True
            
        return self.request.user.role in self.required_roles
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _("Veuillez vous connecter pour accéder à cette page."))
            return super().handle_no_permission()
        messages.error(self.request, _("Vous n'avez pas la permission d'accéder à cette page."))
        return redirect('home')


# Mixins spécifiques pour chaque rôle
class AdminRequiredMixin(RoleRequiredMixin):
    required_roles = ['admin']
    permission_required = 'accounts.manage_users'

class AgentMineraiRequiredMixin(RoleRequiredMixin):
    required_roles = ['agent_minier']
    permission_required = 'accounts.view_extraction'

class SiteManagerRequiredMixin(RoleRequiredMixin):
    required_roles = ['responsable_site']
    permission_required = 'accounts.view_extraction'

class DriverRequiredMixin(RoleRequiredMixin):
    required_roles = ['chauffeur']
    permission_required = 'accounts.view_transport'

class CustomsOfficerRequiredMixin(RoleRequiredMixin):
    required_roles = ['douane']
    permission_required = 'accounts.validate_export'

class EnvironmentOfficerRequiredMixin(RoleRequiredMixin):
    required_roles = ['environnement']
    permission_required = 'accounts.view_environment_metrics'

class ViewerRequiredMixin(RoleRequiredMixin):
    required_roles = ['lecteur']
    permission_required = 'accounts.view_dashboard'


class DashboardMixin(LoginRequiredMixin):
    """Mixin de base pour les vues de tableau de bord"""
    login_url = 'login'
    template_name = 'dashboard/base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['is_dark_mode'] = self.request.user.dark_mode if hasattr(self.request.user, 'dark_mode') else False
        return context
    
    def get_template_names(self):
        """Retourne le template spécifique au rôle de l'utilisateur"""
        if not self.request.user.is_authenticated:
            return [self.template_name]
            
        role_templates = {
            'admin': 'dashboard/admin/base.html',
            'agent_minier': 'dashboard/agent/base.html',
            'responsable_site': 'dashboard/site_manager/base.html',
            'chauffeur': 'dashboard/driver/base.html',
            'douane': 'dashboard/customs/base.html',
            'environnement': 'dashboard/environment/base.html',
            'lecteur': 'dashboard/viewer/base.html',
        }
        
        return [role_templates.get(self.request.user.role, self.template_name)]


class PermissionRequiredMixin(UserPassesTestMixin):
    """Vérifie que l'utilisateur a une permission spécifique"""
    permission_required = None
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if not self.permission_required:
            return True
        return self.request.user.has_perm(self.permission_required)
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, _("Veuillez vous connecter pour accéder à cette page."))
            return redirect(f"{reverse_lazy('login')}?next={self.request.path}")
        messages.error(self.request, _("Vous n'avez pas la permission d'accéder à cette page."))
        return redirect('home')
