from django import forms
from django.core.mail import send_mail
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 px-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Votre nom complet',
            'required': 'required'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-gray-300 px-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'votre@email.com',
            'required': 'required'
        })
    )
    
    subject = forms.ChoiceField(
        choices=[
            ('support', 'Support technique'),
            ('sales', 'Service commercial'),
            ('partnership', 'Partenariat'),
            ('other', 'Autre')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 px-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'required': 'required'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full border border-gray-300 px-3 py-2 rounded-lg shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500',
            'rows': 4,
            'placeholder': 'Votre message...',
            'required': 'required'
        })
    )
    
    def send_email(self):
        subject = f"[SGM Contact] {self.cleaned_data['subject']} - {self.cleaned_data['name']}"
        message = f"""
        Nom: {self.cleaned_data['name']}
        Email: {self.cleaned_data['email']}
        Sujet: {self.cleaned_data['subject']}
        
        Message:
        {self.cleaned_data['message']}
        """
        
        # Envoyer l'email à l'administrateur
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
        
        # Envoyer une confirmation à l'utilisateur
        confirmation_subject = f"Confirmation de réception - {self.cleaned_data['subject']}"
        confirmation_message = f"""
        Bonjour {self.cleaned_data['name']},
        
        Nous avons bien reçu votre message concernant "{self.cleaned_data['subject']}".
        Notre équipe vous répondra dans les plus brefs délais.
        
        Cordialement,
        L'équipe SGM
        """
        
        send_mail(
            subject=confirmation_subject,
            message=confirmation_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.cleaned_data['email']],
            fail_silently=False,
        )

from accounts.models import CustomUser

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
