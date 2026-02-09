from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Import du modèle CustomUser
from accounts.models import CustomUser
from django.utils import timezone
from django.conf import settings

User = get_user_model()

class DashboardMetric(models.Model):
    """Modèle pour stocker les métriques du tableau de bord"""
    
    class MetricType(models.TextChoices):
        EXTRACTION_TOTAL = 'extraction_total', _('Total extractions')
        EXTRACTION_MONTHLY = 'extraction_monthly', _('Extractions mensuelles')
        TRANSPORT_TOTAL = 'transport_total', _('Total transports')
        TRANSPORT_PENDING = 'transport_pending', _('Transports en attente')
        EXPORT_TOTAL = 'export_total', _('Total exports')
        EXPORT_PENDING = 'export_pending', _('Exports en attente')
        SITE_ACTIVE = 'site_active', _('Sites actifs')
        ALERTS_OPEN = 'alerts_open', _('Alertes ouvertes')
        REVENUE_MONTHLY = 'revenue_monthly', _('Revenu mensuel')
        USER_ACTIVITY = 'user_activity', _('Activité utilisateur')
    
    metric_type = models.CharField(
        max_length=50, 
        choices=MetricType.choices, 
        verbose_name=_("Type de métrique")
    )
    value = models.JSONField(verbose_name=_("Valeur"))  # Peut stocker des valeurs simples ou complexes
    
    # Période couverte par la métrique
    period_start = models.DateField(verbose_name=_("Début de période"))
    period_end = models.DateField(verbose_name=_("Fin de période"))
    
    # Métadonnées
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_metrics',
        verbose_name=_("Créé par")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Créé le"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Mis à jour le"))
    
    # Pour le suivi des modifications
    version = models.PositiveIntegerField(default=1, verbose_name=_("Version"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    
    class Meta:
        verbose_name = _("Métrique du tableau de bord")
        verbose_name_plural = _("Métriques du tableau de bord")
        ordering = ['-period_end', 'metric_type']
        indexes = [
            models.Index(fields=['metric_type', '-period_end']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['metric_type', 'period_start', 'period_end'], 
                name='unique_metric_period'
            )
        ]
    
    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.period_start} à {self.period_end}"
    
    def save(self, *args, **kwargs):
        # Incrémenter la version à chaque mise à jour
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_latest_metric(cls, metric_type, default=None):
        """Récupère la dernière métrique d'un type donné"""
        try:
            return cls.objects.filter(
                metric_type=metric_type,
                is_active=True
            ).latest('period_end')
        except cls.DoesNotExist:
            return default


class DashboardWidget(models.Model):
    """Modèle pour les widgets personnalisables des tableaux de bord"""
    
    class WidgetType(models.TextChoices):
        CHART_LINE = 'chart_line', _('Graphique linéaire')
        CHART_BAR = 'chart_bar', _('Graphique à barres')
        CHART_PIE = 'chart_pie', _('Graphique circulaire')
        METRIC_CARD = 'metric_card', _('Carte de métrique')
        DATA_TABLE = 'data_table', _('Tableau de données')
        ACTIVITY_FEED = 'activity_feed', _('Flux d\'activité')
        ALERT_LIST = 'alert_list', _('Liste d\'alertes')
        MAP_VIEW = 'map_view', _('Vue carte')
    
    class WidgetSize(models.TextChoices):
        SMALL = 'small', _('Petit (1x1)')
        MEDIUM = 'medium', _('Moyen (2x1)')
        LARGE = 'large', _('Grand (2x2)')
        XLARGE = 'xlarge', _('Très grand (3x2)')
    
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    widget_type = models.CharField(
        max_length=50, 
        choices=WidgetType.choices,
        verbose_name=_("Type de widget")
    )
    size = models.CharField(
        max_length=10, 
        choices=WidgetSize.choices, 
        default=WidgetSize.MEDIUM,
        verbose_name=_("Taille")
    )
    
    # Configuration du widget (stockée en JSON)
    config = models.JSONField(
        default=dict,
        verbose_name=_("Configuration")
    )
    
    # Filtres par défaut
    filters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Filtres")
    )
    
    # Ordre d'affichage
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    
    # Visibilité et accès
    is_visible = models.BooleanField(default=True, verbose_name=_("Visible"))
    roles = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='dashboard_widgets',
        verbose_name=_("Rôles autorisés")
    )
    
    # Métadonnées
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_widgets',
        verbose_name=_("Créé par")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Créé le"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Mis à jour le"))
    
    class Meta:
        verbose_name = _("Widget de tableau de bord")
        verbose_name_plural = _("Widgets de tableaux de bord")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def is_system_widget(self):
        """Vérifie si c'est un widget système qui ne peut pas être supprimé"""
        return self.config.get('system', False)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dashboard:widget_detail', kwargs={'pk': self.pk})


class DashboardLayout(models.Model):
    """Modèle pour stocker la disposition personnalisée des tableaux de bord"""
    
    class LayoutType(models.TextChoices):
        DEFAULT = 'default', _('Défaut')
        CUSTOM = 'custom', _('Personnalisé')
        ROLE_BASED = 'role_based', _('Par rôle')
    
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    layout_type = models.CharField(
        max_length=20,
        choices=LayoutType.choices,
        default=LayoutType.CUSTOM,
        verbose_name=_("Type de disposition")
    )
    
    # Configuration de la disposition (stockée en JSON)
    config = models.JSONField(
        default=dict,
        verbose_name=_("Configuration de la disposition")
    )
    
    # Widgets inclus dans cette disposition
    widgets = models.ManyToManyField(
        DashboardWidget,
        through='DashboardWidgetPosition',
        related_name='layouts',
        verbose_name=_("Widgets")
    )
    
    # Rôle utilisateur associé (si applicable)
    role = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        choices=User.Role.choices,
        verbose_name=_("Rôle utilisateur")
    )
    
    # Métadonnées
    is_default = models.BooleanField(default=False, verbose_name=_("Disposition par défaut"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_layouts',
        verbose_name=_("Créé par")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Créé le"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Mis à jour le"))
    
    class Meta:
        verbose_name = _("Disposition de tableau de bord")
        verbose_name_plural = _("Dispositions de tableaux de bord")
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['role'], 
                condition=models.Q(is_default=True),
                name='unique_default_role_layout'
            )
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule disposition par défaut par rôle
        if self.is_default and self.role:
            DashboardLayout.objects.filter(
                role=self.role, 
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class DashboardWidgetPosition(models.Model):
    """Modèle pour stocker la position des widgets dans une disposition"""
    
    layout = models.ForeignKey(
        DashboardLayout,
        on_delete=models.CASCADE,
        related_name='widget_positions',
        verbose_name=_("Disposition")
    )
    widget = models.ForeignKey(
        DashboardWidget,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name=_("Widget")
    )
    
    # Position et taille
    row = models.PositiveIntegerField(verbose_name=_("Ligne"))
    col = models.PositiveIntegerField(verbose_name=_("Colonne"))
    size_x = models.PositiveIntegerField(default=1, verbose_name=_("Largeur"))
    size_y = models.PositiveIntegerField(default=1, verbose_name=_("Hauteur"))
    
    # Ordre d'affichage
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    
    # Personnalisation spécifique à cette position
    config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Configuration")
    )
    
    class Meta:
        verbose_name = _("Position de widget")
        verbose_name_plural = _("Positions de widgets")
        ordering = ['order']
        unique_together = [
            ['layout', 'widget'],
            ['layout', 'row', 'col']
        ]
    
    def __str__(self):
        return f"{self.widget.name} - {self.layout.name}"


class DashboardUserSettings(models.Model):
    """Paramètres utilisateur pour les tableaux de bord"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard_settings',
        verbose_name=_("Utilisateur")
    )
    
    # Préférences d'affichage
    theme = models.CharField(
        max_length=50,
        default='light',
        choices=[
            ('light', _('Clair')),
            ('dark', _('Sombre')),
            ('system', _('Système')),
        ],
        verbose_name=_("Thème")
    )
    
    # Disposition personnalisée
    custom_layout = models.ForeignKey(
        DashboardLayout,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_settings',
        verbose_name=_("Disposition personnalisée")
    )
    
    # Préférences de notification
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_("Notifications par email")
    )
    
    # Filtres par défaut
    default_filters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Filtres par défaut")
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Créé le"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Mis à jour le"))
    
    class Meta:
        verbose_name = _("Paramètre utilisateur de tableau de bord")
        verbose_name_plural = _("Paramètres utilisateur des tableaux de bord")
    
    def __str__(self):
        return f"Paramètres de {self.user.username}"


class DashboardActivityLog(models.Model):
    """Journal des activités liées aux tableaux de bord"""
    
    class ActionType(models.TextChoices):
        VIEW = 'view', _('Visualisation')
        CREATE = 'create', _('Création')
        UPDATE = 'update', _('Mise à jour')
        DELETE = 'delete', _('Suppression')
        EXPORT = 'export', _('Export')
        IMPORT = 'import', _('Import')
        SHARE = 'share', _('Partage')
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='dashboard_activities',
        verbose_name=_("Utilisateur")
    )
    
    action = models.CharField(
        max_length=20,
        choices=ActionType.choices,
        verbose_name=_("Action")
    )
    
    # Référence à l'objet concerné (peut être un dashboard, un widget, etc.)
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    
    # Détails supplémentaires
    details = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Détails")
    )
    
    # Informations de requête
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("Adresse IP")
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name=_("User Agent")
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Horodatage")
    )
    
    class Meta:
        verbose_name = _("Journal d'activité du tableau de bord")
        verbose_name_plural = _("Journaux d'activité des tableaux de bord")
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} par {self.user} à {self.timestamp}"
    
    @classmethod
    def log_activity(cls, user, action, obj=None, details=None, request=None):
        """Méthode utilitaire pour enregistrer une activité"""
        from django.contrib.contenttypes.models import ContentType
        
        content_type = None
        object_id = None
        
        if obj is not None:
            content_type = ContentType.objects.get_for_model(obj)
            object_id = obj.pk
        
        ip_address = None
        user_agent = ''
        
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        return cls.objects.create(
            user=user,
            action=action,
            content_type=content_type,
            object_id=object_id,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent
        )


class Report(models.Model):
    """Modèle pour gérer les rapports générés"""
    
    class ReportType(models.TextChoices):
        EXTRACTION_SUMMARY = 'extraction_summary', _('Résumé des extractions')
        TRANSPORT_TRACKING = 'transport_tracking', _('Suivi des transports')
        EXPORT_ANALYSIS = 'export_analysis', _('Analyse des exportations')
        ENVIRONMENT_REPORT = 'environment_report', _('Rapport environnemental')
        FINANCIAL_REPORT = 'financial_report', _('Rapport financier')
        AUDIT_LOG = 'audit_log', _('Journal d\'audit')
        CUSTOM = 'custom', _('Personnalisé')
    
    class FormatType(models.TextChoices):
        PDF = 'pdf', 'PDF'
        EXCEL = 'excel', 'Excel'
        CSV = 'csv', 'CSV'
        JSON = 'json', 'JSON'
        HTML = 'html', 'HTML'
    
    title = models.CharField(max_length=255, verbose_name="Titre")
    report_type = models.CharField(max_length=50, choices=ReportType.choices, verbose_name="Type de rapport")
    format = models.CharField(max_length=10, choices=FormatType.choices, default='pdf',
                            verbose_name="Format")
    
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    
    generated_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True,
                                    verbose_name="Généré par")
    
    file_path = models.FileField(upload_to='reports/%Y/%m/%d/', null=True, blank=True,
                                verbose_name="Chemin du fichier")
    
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="Généré le")
    
    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['report_type', '-generated_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"

