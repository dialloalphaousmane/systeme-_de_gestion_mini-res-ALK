from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    """Modèle User personnalisé pour la plateforme SGM"""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrateur')
        AGENT_MINIER = 'agent_minier', _('Agent Minier')
        RESPONSABLE_SITE = 'responsable_site', _('Responsable Site')
        CHAUFFEUR = 'chauffeur', _('Chauffeur/Transporteur')
        DOUANE = 'douane', _('Responsable Douane')
        ENVIRONNEMENT = 'environnement', _('Responsable Environnement')
        LECTEUR = 'lecteur', _('Lecteur/Visiteur')
    
    ROLE_PERMISSIONS = {
        'admin': [
            'view_dashboard', 'add_user', 'change_user', 'delete_user',
            'view_extraction', 'add_extraction', 'change_extraction',
            'view_transport', 'add_transport', 'change_transport',
            'view_export', 'add_export', 'change_export',
            'view_report', 'generate_report', 'export_data',
        ],
        'agent_minier': [
            'view_dashboard', 'view_extraction', 'add_extraction', 'change_extraction',
            'view_transport', 'view_report',
        ],
        'responsable_site': [
            'view_dashboard', 'view_extraction', 'add_extraction', 'change_extraction',
            'view_transport', 'view_report',
        ],
        'chauffeur': [
            'view_dashboard', 'view_transport', 'update_transport_status',
        ],
        'douane': [
            'view_dashboard', 'validate_export', 'view_export',
        ],
        'environnement': [
            'view_dashboard', 'view_environment_metrics', 'add_environment_alert',
        ],
        'lecteur': [
            'view_dashboard',
        ],
    }
    
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Téléphone"))
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.LECTEUR, 
        verbose_name=_("Rôle")
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        null=True, 
        blank=True,
        verbose_name=_("Photo de profil")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("Dernière IP de connexion"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Créé le"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Modifié le"))
    
    # Champs pour les préférences utilisateur
    dark_mode = models.BooleanField(default=False, verbose_name=_("Mode sombre"))
    receive_notifications = models.BooleanField(default=True, verbose_name=_("Recevoir les notifications"))
    language = models.CharField(
        max_length=10, 
        choices=settings.LANGUAGES, 
        default=settings.LANGUAGE_CODE,
        verbose_name=_("Langue")
    )
    
    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ['-created_at']
        permissions = [
            ('view_dashboard', _('Peut voir le tableau de bord')),
            ('manage_users', _('Peut gérer les utilisateurs')),
            ('view_extraction', _('Peut voir les extractions')),
            ('add_extraction', _('Peut ajouter des extractions')),
            ('change_extraction', _('Peut modifier les extractions')),
            ('view_transport', _('Peut voir les transports')),
            ('update_transport_status', _('Peut mettre à jour le statut des transports')),
            ('validate_export', _('Peut valider les exports')),
            ('generate_report', _('Peut générer des rapports')),
        ]
    
    def __str__(self):
        full_name = self.get_full_name()
        return f"{full_name} ({self.get_role_display()})" if full_name.strip() else self.username
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Mettre à jour les groupes et permissions
        self.update_groups_and_permissions()
    
    def update_groups_and_permissions(self):
        """Met à jour les groupes et permissions en fonction du rôle"""
        # Supprimer tous les groupes existants
        self.groups.clear()
        
        # Créer ou récupérer le groupe correspondant au rôle
        group_name = f"role_{self.role}"
        group, created = Group.objects.get_or_create(name=group_name)
        
        # Ajouter les permissions au groupe
        permissions = self.ROLE_PERMISSIONS.get(self.role, [])
        for perm_codename in permissions:
            try:
                app_label, codename = perm_codename.split('.')
                perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                group.permissions.add(perm)
            except (ValueError, Permission.DoesNotExist):
                # Gérer les permissions personnalisées qui n'ont pas de modèle associé
                pass
        
        # Ajouter l'utilisateur au groupe
        self.groups.add(group)
    
    # Méthodes de vérification de rôle
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    def is_agent_minier(self):
        return self.role == self.Role.AGENT_MINIER
    
    def is_responsable_site(self):
        return self.role == self.Role.RESPONSABLE_SITE
    
    def is_chauffeur(self):
        return self.role == self.Role.CHAUFFEUR
    
    def is_douane(self):
        return self.role == self.Role.DOUANE
    
    def is_environnement(self):
        return self.role == self.Role.ENVIRONNEMENT
    
    def is_lecteur(self):
        return self.role == self.Role.LECTEUR
    
    # Propriétés pratiques pour les templates
    @property
    def is_staff_member(self):
        return self.role in [self.Role.ADMIN, self.Role.AGENT_MINIER, self.Role.RESPONSABLE_SITE]
    
    @property
    def dashboard_url(self):
        """Retourne l'URL du tableau de bord en fonction du rôle"""
        return {
            self.Role.ADMIN: 'admin_dashboard',
            self.Role.AGENT_MINIER: 'agent_dashboard',
            self.Role.RESPONSABLE_SITE: 'site_manager_dashboard',
            self.Role.CHAUFFEUR: 'driver_dashboard',
            self.Role.DOUANE: 'customs_dashboard',
            self.Role.ENVIRONNEMENT: 'environment_dashboard',
            self.Role.LECTEUR: 'viewer_dashboard',
        }.get(self.role, 'home')


@receiver(post_save, sender=CustomUser)
def set_default_permissions(sender, instance, created, **kwargs):
    """Définit les permissions par défaut lors de la création d'un utilisateur"""
    if created:
        instance.update_groups_and_permissions()


class UserActivityLog(models.Model):
    """Historique des activités utilisateurs pour l'audit"""
    
    ACTION_CHOICES = [
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
        ('export', 'Export'),
        ('download', 'Téléchargement'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Action")
    description = models.TextField(verbose_name="Description")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Adresse IP")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date/Heure")
    
    class Meta:
        verbose_name = "Journal d'activité"
        verbose_name_plural = "Journaux d'activité"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.timestamp}"
