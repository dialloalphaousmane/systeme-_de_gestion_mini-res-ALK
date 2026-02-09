from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from accounts.models import CustomUser
from .forms import UserUpdateForm # Nous créerons ce formulaire juste après

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'dashboard/admin/user_form.html'
    success_url = reverse_lazy('dashboard:admin_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Modifier l'utilisateur: {self.object.username}"
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Les informations de l'utilisateur ont été mises à jour avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)