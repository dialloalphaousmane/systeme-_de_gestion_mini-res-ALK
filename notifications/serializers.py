from rest_framework import serializers
from .models import Notification, EmailNotification

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications internes"""
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'recipient_name', 'title', 'message',
                 'notification_type', 'notification_type_display', 'priority',
                 'priority_display', 'related_id', 'is_read', 'read_at', 'sent_at']
        read_only_fields = ['id', 'sent_at']


class EmailNotificationSerializer(serializers.ModelSerializer):
    """Serializer pour les notifications emails"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = EmailNotification
        fields = ['id', 'recipient_email', 'subject', 'body', 'status',
                 'status_display', 'error_message', 'scheduled_for', 'sent_at', 'created_at']
        read_only_fields = ['id', 'created_at']
