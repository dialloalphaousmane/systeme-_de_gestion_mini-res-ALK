from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import qrcode
from io import BytesIO
from django.utils import timezone
from .models import Truck, Transport, TransportLocation
from .serializers import TruckSerializer, TransportSerializer, TransportDetailSerializer, TransportLocationSerializer

class TruckViewSet(viewsets.ModelViewSet):
	queryset = Truck.objects.all()
	serializer_class = TruckSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['registration_number', 'truck_type']
	ordering_fields = ['registration_number', 'status']


class TransportViewSet(viewsets.ModelViewSet):
	queryset = Transport.objects.all()
	permission_classes = [IsAuthenticated]
	search_fields = ['qr_code', 'extraction__site__name']
	ordering_fields = ['departure_date', 'status']
    
	def get_serializer_class(self):
		if self.action == 'retrieve':
			return TransportDetailSerializer
		return TransportSerializer
    
	@action(detail=False, methods=['post'])
	def record_departure(self, request):
		qr_code = request.data.get('qr_code')
		try:
			transport = Transport.objects.get(qr_code=qr_code)
			if transport.status != 'depart_planifie':
				return Response({'error': 'Le départ ne peut pas être enregistré'}, 
							  status=status.HTTP_400_BAD_REQUEST)
			transport.status = 'en_transit'
			transport.departure_date = timezone.now()
			transport.save()
			serializer = TransportSerializer(transport)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Transport.DoesNotExist:
			return Response({'error': 'Transport non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    
	@action(detail=False, methods=['post'])
	def record_arrival(self, request):
		qr_code = request.data.get('qr_code')
		try:
			transport = Transport.objects.get(qr_code=qr_code)
			if transport.status != 'en_transit':
				return Response({'error': 'Ce transport n\'est pas en transit'}, 
							  status=status.HTTP_400_BAD_REQUEST)
			transport.status = 'arrive'
			transport.arrival_date = timezone.now()
			transport.save()
			serializer = TransportSerializer(transport)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Transport.DoesNotExist:
			return Response({'error': 'Transport non trouvé'}, status=status.HTTP_404_NOT_FOUND)
