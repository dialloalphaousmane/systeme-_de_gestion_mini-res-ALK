from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Notification, EmailNotification
from .serializers import NotificationSerializer, EmailNotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
	serializer_class = NotificationSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['title', 'message']
	ordering_fields = ['sent_at']
    
	def get_queryset(self):
		return Notification.objects.filter(recipient=self.request.user)
    
	@action(detail=False, methods=['get'])
	def unread(self, request):
		notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-sent_at')
		serializer = self.get_serializer(notifications, many=True)
		return Response(serializer.data)
    
	@action(detail=True, methods=['post'])
	def mark_as_read(self, request, pk=None):
		notification = self.get_object()
		notification.mark_as_read()
		serializer = self.get_serializer(notification)
		return Response(serializer.data, status=status.HTTP_200_OK)
    
	@action(detail=False, methods=['post'])
	def mark_all_as_read(self, request):
		notifications = Notification.objects.filter(recipient=request.user, is_read=False)
		for notification in notifications:
			notification.mark_as_read()
		return Response({'detail': f'{len(notifications)} notifications marquées comme lues'}, status=status.HTTP_200_OK)
    
	@action(detail=False, methods=['get'])
	def count_unread(self, request):
		count = Notification.objects.filter(recipient=request.user, is_read=False).count()
		return Response({'unread_count': count})


class EmailNotificationViewSet(viewsets.ModelViewSet):
	queryset = EmailNotification.objects.all()
	serializer_class = EmailNotificationSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['recipient_email', 'subject']
	ordering_fields = ['created_at', 'status']
    
	@action(detail=True, methods=['post'])
	def resend(self, request, pk=None):
		email_notif = self.get_object()
		if email_notif.status != 'failed':
			return Response({'error': 'Seuls les emails échoués peuvent être renvoyés'}, status=status.HTTP_400_BAD_REQUEST)
		email_notif.status = 'pending'
		email_notif.error_message = ''
		email_notif.save()
		serializer = self.get_serializer(email_notif)
		return Response(serializer.data, status=status.HTTP_200_OK)
