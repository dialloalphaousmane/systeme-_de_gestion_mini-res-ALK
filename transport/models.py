from django.db import models
from django.core.validators import MinValueValidator
import uuid
from extraction.models import Extraction
from accounts.models import CustomUser

class Truck(models.Model):
    """Modèle pour enregistrer les camions/transporteurs"""
    
    STATUS_CHOICES = [
        ('actif', 'Actif'),
        ('maintenance', 'En maintenance'),
        ('retire', 'Retiré'),
    ]
    
    registration_number = models.CharField(max_length=50, unique=True, verbose_name="Immatriculation")
    truck_type = models.CharField(max_length=100, verbose_name="Type de camion")
    capacity_tonnes = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Capacité (tonnes)",
                                         validators=[MinValueValidator(0)])
    owner = models.CharField(max_length=200, verbose_name="Propriétaire")
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                              limit_choices_to={'role': 'chauffeur'}, verbose_name="Chauffeur assigné")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actif', 
                            verbose_name="Statut")
    inspection_date = models.DateField(null=True, blank=True, verbose_name="Dernière inspection")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Camion"
        verbose_name_plural = "Camions"
        ordering = ['registration_number']
    
    def __str__(self):
        return f"{self.registration_number} - {self.truck_type}"


class Transport(models.Model):
    """Modèle pour enregistrer les transports/cargaisons"""
    
    STATUS_CHOICES = [
        ('depart_planifie', 'Départ planifié'),
        ('en_transit', 'En transit'),
        ('arrive', 'Arrivé'),
        ('annule', 'Annulé'),
    ]
    
    qr_code = models.CharField(max_length=100, unique=True, default=uuid.uuid4, 
                              verbose_name="QR Code unique")
    extraction = models.ForeignKey(Extraction, on_delete=models.CASCADE, related_name='transports',
                                 verbose_name="Extraction")
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True, 
                            verbose_name="Camion")
    departure_location = models.CharField(max_length=200, verbose_name="Lieu de départ")
    destination = models.CharField(max_length=200, verbose_name="Destination")
    
    departure_date = models.DateTimeField(null=True, blank=True, verbose_name="Date/heure de départ")
    arrival_date = models.DateTimeField(null=True, blank=True, verbose_name="Date/heure d'arrivée")
    
    quantity_transported = models.DecimalField(max_digits=15, decimal_places=2, 
                                             verbose_name="Quantité transportée (tonnes)",
                                             validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='depart_planifie',
                            verbose_name="Statut")
    
    driver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                             limit_choices_to={'role': 'chauffeur'}, verbose_name="Chauffeur")
    gps_tracking = models.BooleanField(default=False, verbose_name="Suivi GPS activé")
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    class Meta:
        verbose_name = "Transport"
        verbose_name_plural = "Transports"
        ordering = ['-departure_date']
        indexes = [
            models.Index(fields=['qr_code']),
            models.Index(fields=['status']),
            models.Index(fields=['extraction']),
        ]
    
    def __str__(self):
        return f"Transport {self.qr_code} - {self.extraction.site.name}"


class TransportLocation(models.Model):
    """Modèle pour enregistrer les positions GPS des transports"""
    
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='locations',
                                 verbose_name="Transport")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitude")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date/Heure")
    
    class Meta:
        verbose_name = "Position transport"
        verbose_name_plural = "Positions transport"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.transport.qr_code} - {self.timestamp}"

