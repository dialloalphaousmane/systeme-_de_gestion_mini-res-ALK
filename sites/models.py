from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser

class Site(models.Model):
    """Modèle pour les sites miniers"""
    
    MINERAL_TYPES = [
        ('bauxite', 'Bauxite'),
        ('or', 'Or'),
        ('diamant', 'Diamant'),
        ('fer', 'Fer'),
        ('cuivre', 'Cuivre'),
        ('autre', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('clos', 'Clôturé'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom du site")
    mineral_type = models.CharField(max_length=20, choices=MINERAL_TYPES, verbose_name="Type de minerai")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitude")
    address = models.TextField(verbose_name="Adresse")
    region = models.CharField(max_length=100, verbose_name="Région")
    manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                               limit_choices_to={'role': 'responsable_site'}, verbose_name="Responsable")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actif', verbose_name="Statut")
    capacity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Capacité de production (tonnes)", 
                                   validators=[MinValueValidator(0)])
    operational_since = models.DateField(verbose_name="En opération depuis")
    license_number = models.CharField(max_length=100, unique=True, verbose_name="Numéro de permis")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Site minier"
        verbose_name_plural = "Sites miniers"
        ordering = ['name']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['mineral_type']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_mineral_type_display()})"


class SiteOperationHistory(models.Model):
    """Historique des opérations pour chaque site"""
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='operation_history', 
                            verbose_name="Site")
    description = models.TextField(verbose_name="Description")
    recorded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, 
                                   verbose_name="Enregistré par")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date/Heure")
    
    class Meta:
        verbose_name = "Historique d'opération"
        verbose_name_plural = "Historiques d'opération"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['site', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.site} - {self.timestamp}"
