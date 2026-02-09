from django.db import models
from accounts.models import CustomUser

class Notification(models.Model):
    """Modèle pour gérer les notifications internes"""
    
    NOTIFICATION_TYPES = [
        ('extraction', 'Extraction'),
        ('transport', 'Transport'),
        ('export', 'Export'),
        ('environment', 'Environnement'),
        ('alert', 'Alerte'),
        ('system', 'Système'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('critical', 'Critique'),
    ]
    
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                                 related_name='notifications', verbose_name="Destinataire")
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, 
                                        verbose_name="Type de notification")
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium',
                               verbose_name="Priorité")
    
    related_id = models.IntegerField(null=True, blank=True, verbose_name="ID de l'objet lié")
    
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Lu le")
    
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Envoyé le")
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['-sent_at']),
        ]
    
    def __str__(self):
        return f"[{self.notification_type}] {self.title} → {self.recipient.username}"
    
    def mark_as_read(self):
        """Marquer la notification comme lue"""
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class EmailNotification(models.Model):
    """Modèle pour enregistrer les emails envoyés"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('sent', 'Envoyé'),
        ('failed', 'Échoué'),
    ]
    
    recipient_email = models.EmailField(verbose_name="Email du destinataire")
    subject = models.CharField(max_length=255, verbose_name="Sujet")
    body = models.TextField(verbose_name="Corps du message")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending',
                            verbose_name="Statut")
    error_message = models.TextField(blank=True, verbose_name="Message d'erreur")
    
    scheduled_for = models.DateTimeField(null=True, blank=True, verbose_name="Programmé pour")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Envoyé le")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    
    class Meta:
        verbose_name = "Notification email"
        verbose_name_plural = "Notifications emails"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'scheduled_for']),
        ]
    
    def __str__(self):
        return f"{self.subject} → {self.recipient_email}"

