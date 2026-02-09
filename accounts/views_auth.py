from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordResetView as BasePasswordResetView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import UserActivityLog

class CustomLoginView(BaseLoginView):
    """Vue personnalisée pour la connexion des utilisateurs"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        # Enregistrement de l'activité
        user = form.get_user()
        UserActivityLog.objects.create(
            user=user,
            action='login',
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Message de bienvenue
        messages.success(
            self.request, 
            _('Bienvenue, %(username)s !') % {'username': user.get_short_name() or user.username}
        )
        
        return super().form_valid(form)
    
    def get_success_url(self):
        # Rediriger vers le tableau de bord approprié
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('dashboard:dashboard')


class CustomLogoutView(BaseLogoutView):
    """Vue personnalisée pour la déconnexion des utilisateurs"""
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        # Enregistrement de l'activité avant la déconnexion
        if request.user.is_authenticated:
            UserActivityLog.objects.create(
                user=request.user,
                action='logout',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        response = super().dispatch(request, *args, **kwargs)
        messages.info(request, _('Vous avez été déconnecté avec succès.'))
        return response


class CustomPasswordResetView(BasePasswordResetView):
    """Vue personnalisée pour la réinitialisation du mot de passe"""
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def form_valid(self, form):
        # Enregistrement de la tentative de réinitialisation
        email = form.cleaned_data['email']
        try:
            user = self.get_user(email)
            UserActivityLog.objects.create(
                user=user,
                action='password_reset_request',
                ip_address=self.request.META.get('REMOTE_ADDR'),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
        except Exception:
            pass  # Ne pas révéler si l'email existe ou non
            
        messages.info(
            self.request,
            _("Si un compte existe avec l'adresse email que vous avez fournie, "
              "vous recevrez bientôt un email avec les instructions pour réinitialiser votre mot de passe.")
        )
        return super().form_valid(form)


class CustomPasswordResetDoneView(BasePasswordResetDoneView):
    """Vue de confirmation d'envoi d'email de réinitialisation"""
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(BasePasswordResetConfirmView):
    """Vue de confirmation de réinitialisation du mot de passe"""
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    
    def form_valid(self, form):
        # Enregistrement du changement de mot de passe
        response = super().form_valid(form)
        
        if self.user.is_authenticated:
            UserActivityLog.objects.create(
                user=self.user,
                action='password_reset_confirm',
                ip_address=self.request.META.get('REMOTE_ADDR'),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
        
        return response


class CustomPasswordResetCompleteView(BasePasswordResetCompleteView):
    """Vue de confirmation de réinitialisation du mot de passe terminée"""
    template_name = 'accounts/password_reset_complete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = reverse_lazy('accounts:login')
        return context
