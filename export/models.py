from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from transport.models import Transport
from accounts.models import CustomUser

class Export(models.Model):
    """Modèle pour gérer les exportations"""
    
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée'),
        ('expedie', 'Expédié'),
        ('livre', 'Livré'),
    ]
    
    PAYMENT_STATUS = [
        ('en_attente', 'En attente'),
        ('partiellement_paye', 'Partiellement payé'),
        ('entierement_paye', 'Entièrement payé'),
    ]
    
    reference_number = models.CharField(max_length=100, unique=True, verbose_name="Numéro de référence")
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='exports',
                                verbose_name="Transport")
    
    quantity_exported = models.DecimalField(max_digits=15, decimal_places=2,
                                           verbose_name="Quantité exportée (tonnes)",
                                           validators=[MinValueValidator(0)])
    
    destination_country = models.CharField(max_length=100, verbose_name="Pays de destination")
    buyer = models.CharField(max_length=200, verbose_name="Acheteur")
    
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix unitaire ($)",
                                    validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant total ($)",
                                      validators=[MinValueValidator(0)])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente',
                            verbose_name="Statut")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='en_attente',
                                    verbose_name="Statut du paiement")
    
    export_date = models.DateField(verbose_name="Date d'export")
    expected_delivery = models.DateField(null=True, blank=True, verbose_name="Livraison prévue")
    actual_delivery = models.DateField(null=True, blank=True, verbose_name="Livraison réelle")
    
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                   limit_choices_to={'role': 'douane'}, 
                                   verbose_name="Approuvé par", related_name="approved_exports")
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Export"
        verbose_name_plural = "Exports"
        ordering = ['-export_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['-export_date']),
        ]
    
    def __str__(self):
        return f"Export {self.reference_number} - {self.transport.extraction.site.name}"


class ExportDocument(models.Model):
    """Modèle pour gérer les documents d'export"""
    
    DOC_TYPES = [
        ('certificate', 'Certificat d\'origine'),
        ('invoice', 'Facture'),
        ('bill_of_lading', 'Connaissement'),
        ('packing_list', 'Liste de colisage'),
        ('inspection_report', 'Rapport d\'inspection'),
        ('customs_clearance', 'Dédouanement'),
        ('other', 'Autre'),
    ]
    
    export = models.ForeignKey(Export, on_delete=models.CASCADE, related_name='documents',
                             verbose_name="Export")
    document_type = models.CharField(max_length=50, choices=DOC_TYPES, verbose_name="Type de document")
    document_file = models.FileField(upload_to='export_documents/%Y/%m/%d/',
                                    validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xlsx'])],
                                    verbose_name="Fichier")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                   verbose_name="Téléchargé par")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Téléchargé le")
    
    class Meta:
        verbose_name = "Document d'export"
        verbose_name_plural = "Documents d'export"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.export.reference_number} - {self.get_document_type_display()}"

