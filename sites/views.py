from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Site, SiteOperationHistory
from .serializers import SiteSerializer, SiteDetailSerializer, SiteOperationHistorySerializer

class SiteViewSet(viewsets.ModelViewSet):
	"""ViewSet pour gérer les sites miniers"""
	queryset = Site.objects.all()
	permission_classes = [IsAuthenticated]
	search_fields = ['name', 'region', 'mineral_type']
	ordering_fields = ['name', 'created_at', 'status']
    
	def get_serializer_class(self):
		"""Utiliser le serializer détaillé pour le retrieve"""
		if self.action == 'retrieve':
			return SiteDetailSerializer
		return SiteSerializer
    
	@action(detail=True, methods=['post'])
	def log_operation(self, request, pk=None):
		"""Ajouter une note à l'historique des opérations"""
		site = self.get_object()
		description = request.data.get('description', '')
        
		if not description:
			return Response({'error': 'Description requise'}, 
						  status=status.HTTP_400_BAD_REQUEST)
        
		operation = SiteOperationHistory.objects.create(
			site=site,
			description=description,
			recorded_by=request.user
		)
		serializer = SiteOperationHistorySerializer(operation)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
    
	@action(detail=True, methods=['get'])
	def statistics(self, request, pk=None):
		"""Obtenir les statistiques d'un site"""
		site = self.get_object()
		from extraction.models import Extraction
        
		stats = {
			'site_name': site.name,
			'total_extractions': Extraction.objects.filter(site=site).count(),
			'total_quantity': sum(e.quantity_tonnes for e in 
								 Extraction.objects.filter(site=site)),
		}
		return Response(stats)
