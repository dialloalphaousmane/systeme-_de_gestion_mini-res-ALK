from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import EnvironmentMeasure, EnvironmentAlert, EnvironmentThreshold
from .serializers import (EnvironmentMeasureSerializer, EnvironmentAlertSerializer,
						 EnvironmentThresholdSerializer)

class EnvironmentMeasureViewSet(viewsets.ModelViewSet):
	queryset = EnvironmentMeasure.objects.all()
	serializer_class = EnvironmentMeasureSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['site__name', 'measurement_type']
	ordering_fields = ['measurement_date']
    
	def perform_create(self, serializer):
		measure = serializer.save(measured_by=self.request.user)
		self._check_thresholds(measure)
    
	@staticmethod
	def _check_thresholds(measure):
		try:
			threshold = EnvironmentThreshold.objects.get(measurement_type=measure.measurement_type)
			if measure.value > threshold.critical_threshold:
				severity = 'critical'
			elif measure.value > threshold.danger_threshold:
				severity = 'danger'
			elif measure.value > threshold.warning_threshold:
				severity = 'warning'
			else:
				return
			EnvironmentAlert.objects.create(
				site=measure.site,
				measure=measure,
				title=f"Alerte {measure.get_measurement_type_display()}",
				description=f"Seuil de {severity} dépassé",
				threshold_value=getattr(threshold, f'{severity}_threshold'),
				actual_value=measure.value,
				severity=severity
			)
		except EnvironmentThreshold.DoesNotExist:
			pass


class EnvironmentAlertViewSet(viewsets.ModelViewSet):
	queryset = EnvironmentAlert.objects.all()
	serializer_class = EnvironmentAlertSerializer
	permission_classes = [IsAuthenticated]
	search_fields = ['site__name', 'severity']
	ordering_fields = ['triggered_at', 'severity']
    
	def get_queryset(self):
		queryset = super().get_queryset()
		status_filter = self.request.query_params.get('status', 'active')
		if status_filter:
			queryset = queryset.filter(status=status_filter)
		return queryset
    
	@action(detail=True, methods=['post'])
	def resolve(self, request, pk=None):
		alert = self.get_object()
		alert.status = 'resolved'
		from django.utils import timezone
		alert.resolved_at = timezone.now()
		alert.save()
		serializer = EnvironmentAlertSerializer(alert)
		return Response(serializer.data, status=status.HTTP_200_OK)


class EnvironmentThresholdViewSet(viewsets.ModelViewSet):
	queryset = EnvironmentThreshold.objects.all()
	serializer_class = EnvironmentThresholdSerializer
	permission_classes = [IsAuthenticated]
