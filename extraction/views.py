from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Extraction, Stock
from .serializers import ExtractionSerializer, StockSerializer

class ExtractionViewSet(viewsets.ModelViewSet):
	"""ViewSet pour gérer les extractions"""
	queryset = Extraction.objects.all()
	serializer_class = ExtractionSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['site__name', 'status']
	ordering_fields = ['extraction_date', 'quantity_tonnes']
    
	def perform_create(self, serializer):
		"""Créer une extraction et mettre à jour le stock"""
		extraction = serializer.save()
		self._update_stock(extraction)
    
	def perform_update(self, serializer):
		"""Mettre à jour une extraction et le stock"""
		extraction = serializer.save()
		self._update_stock(extraction)
    
	@staticmethod
	def _update_stock(extraction):
		"""Mettre à jour le stock du site"""
		stock, created = Stock.objects.get_or_create(site=extraction.site)
        
		# Recalculer le stock total pour le site
		total = Extraction.objects.filter(
			site=extraction.site,
			status='completee'
		).aggregate(total=models.Sum('quantity_tonnes'))['total'] or 0
        
		stock.quantity_in_stock = total
		stock.save()
    
	@action(detail=False, methods=['get'])
	def by_site(self, request):
		"""Récupérer les extractions par site"""
		site_id = request.query_params.get('site_id')
		if not site_id:
			return Response({'error': 'site_id requis'}, 
						  status=status.HTTP_400_BAD_REQUEST)
        
		extractions = Extraction.objects.filter(site_id=site_id)
		serializer = self.get_serializer(extractions, many=True)
		return Response(serializer.data)


class StockViewSet(viewsets.ReadOnlyModelViewSet):
	"""ViewSet pour consulter les stocks"""
	queryset = Stock.objects.all()
	serializer_class = StockSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['site__name']
	ordering_fields = ['quantity_in_stock']
