from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from sites.models import Site
from accounts.models import CustomUser

class EnvironmentMeasure(models.Model):
    """Modèle pour enregistrer les mesures environnementales"""
    
    MEASUREMENT_TYPES = [
        ('pm25', 'PM2.5 (μg/m³)'),
        ('pm10', 'PM10 (μg/m³)'),
        ('co2', 'CO2 (ppm)'),
        ('noise', 'Bruit (dB)'),
        ('water_ph', 'pH de l\'eau'),
        ('water_turbidity', 'Turbidité (NTU)'),
        ('soil_quality', 'Qualité du sol'),
        ('air_quality', 'Qualité de l\'air'),
    ]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='environment_measures',
                            verbose_name="Site")
    measurement_type = models.CharField(max_length=50, choices=MEASUREMENT_TYPES, 
                                       verbose_name="Type de mesure")
    value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Valeur")
    unit = models.CharField(max_length=20, verbose_name="Unité")
    
    measurement_date = models.DateTimeField(verbose_name="Date/heure de mesure")
    measured_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                   limit_choices_to={'role': 'environnement'},
                                   verbose_name="Mesuré par")
    
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu de mesure")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    
    class Meta:
        verbose_name = "Mesure environnementale"
        verbose_name_plural = "Mesures environnementales"
        ordering = ['-measurement_date']
        indexes = [
            models.Index(fields=['site', '-measurement_date']),
            models.Index(fields=['measurement_type']),
        ]
    
    def __str__(self):
        return f"{self.site.name} - {self.get_measurement_type_display()}: {self.value} {self.unit}"


class EnvironmentAlert(models.Model):
    """Modèle pour enregistrer les alertes environnementales"""
    
    SEVERITY_LEVELS = [
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('danger', 'Danger'),
        ('critical', 'Critique'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('resolved', 'Résolu'),
        ('acknowledged', 'Reconnu'),
    ]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='environment_alerts',
                            verbose_name="Site")
    measure = models.ForeignKey(EnvironmentMeasure, on_delete=models.SET_NULL, null=True,
                               verbose_name="Mesure")
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    
    threshold_value = models.DecimalField(max_digits=10, decimal_places=3, 
                                         verbose_name="Seuil dépassé")
    actual_value = models.DecimalField(max_digits=10, decimal_places=3, 
                                      verbose_name="Valeur réelle")
    
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='warning',
                               verbose_name="Niveau de sévérité")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active',
                            verbose_name="Statut")
    
    triggered_at = models.DateTimeField(auto_now_add=True, verbose_name="Déclenché le")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Résolu le")
    
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   limit_choices_to={'role': 'environnement'},
                                   verbose_name="Assigné à", related_name="assigned_alerts")
    
    class Meta:
        verbose_name = "Alerte environnementale"
        verbose_name_plural = "Alertes environnementales"
        ordering = ['-triggered_at']
        indexes = [
            models.Index(fields=['site', 'status']),
            models.Index(fields=['severity']),
        ]
    
    def __str__(self):
        return f"[{self.severity.upper()}] {self.title} - {self.site.name}"


class EnvironmentThreshold(models.Model):
    """Modèle pour définir les seuils limites par type de mesure"""
    
    measurement_type = models.CharField(max_length=50, unique=True, verbose_name="Type de mesure")
    warning_threshold = models.DecimalField(max_digits=10, decimal_places=3, 
                                           verbose_name="Seuil d'avertissement")
    danger_threshold = models.DecimalField(max_digits=10, decimal_places=3, 
                                          verbose_name="Seuil de danger")
    critical_threshold = models.DecimalField(max_digits=10, decimal_places=3, 
                                           verbose_name="Seuil critique")
    unit = models.CharField(max_length=20, verbose_name="Unité")
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Seuil environnemental"
        verbose_name_plural = "Seuils environnementaux"
    
    def __str__(self):
        return f"{self.measurement_type} - Limites: {self.warning_threshold}/{self.danger_threshold}/{self.critical_threshold}"

