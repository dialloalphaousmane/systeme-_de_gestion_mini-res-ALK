from django.db import models
from django.core.validators import MinValueValidator
from sites.models import Site
from accounts.models import CustomUser

class Extraction(models.Model):
    """Modèle pour enregistrer les extractions minières"""
    
    STATUS_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('completee', 'Complétée'),
        ('annulee', 'Annulée'),
    ]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='extractions', 
                            verbose_name="Site")
    extraction_date = models.DateField(verbose_name="Date d'extraction")
    quantity_tonnes = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Quantité (tonnes)",
                                         validators=[MinValueValidator(0)])
    quality_grade = models.CharField(max_length=50, verbose_name="Grade de qualité", blank=True)
    operator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                limit_choices_to={'role__in': ['agent_minier', 'responsable_site']},
                                verbose_name="Opérateur")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planifiee', 
                            verbose_name="Statut")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Extraction"
        verbose_name_plural = "Extractions"
        ordering = ['-extraction_date']
        indexes = [
            models.Index(fields=['site', '-extraction_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.site.name} - {self.extraction_date} ({self.quantity_tonnes} tonnes)"


class Stock(models.Model):
    """Modèle pour gérer les stocks de minérais"""
    
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name='stock', 
                               verbose_name="Site")
    quantity_in_stock = models.DecimalField(max_digits=15, decimal_places=2, 
                                           verbose_name="Quantité en stock (tonnes)",
                                           validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
    
    def __str__(self):
        return f"Stock - {self.site.name}: {self.quantity_in_stock} tonnes"

