from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Export, ExportDocument
from .serializers import ExportSerializer, ExportDetailSerializer, ExportDocumentSerializer

class ExportViewSet(viewsets.ModelViewSet):
	"""ViewSet pour gérer les exports"""
	queryset = Export.objects.all()
	permission_classes = [IsAuthenticated]
	search_fields = ['reference_number', 'transport__extraction__site__name']
	ordering_fields = ['export_date', 'status']
    
	def get_serializer_class(self):
		if self.action == 'retrieve':
			return ExportDetailSerializer
		return ExportSerializer
    
	@action(detail=True, methods=['post'])
	def approve(self, request, pk=None):
		export = self.get_object()
		if request.user.role != 'douane':
			return Response({'error': 'Seul la douane peut approuver'}, status=status.HTTP_403_FORBIDDEN)
		export.status = 'approuvee'
		export.approved_by = request.user
		export.save()
		serializer = ExportSerializer(export)
		return Response(serializer.data, status=status.HTTP_200_OK)
    
	@action(detail=True, methods=['post'])
	def reject(self, request, pk=None):
		export = self.get_object()
		if request.user.role != 'douane':
			return Response({'error': 'Seul la douane peut rejeter'}, status=status.HTTP_403_FORBIDDEN)
		export.status = 'rejetee'
		export.save()
		serializer = ExportSerializer(export)
		return Response(serializer.data, status=status.HTTP_200_OK)
    
	@action(detail=True, methods=['post'])
	def upload_document(self, request, pk=None):
		export = self.get_object()
		document_type = request.data.get('document_type')
		file = request.FILES.get('document_file')
		if not document_type or not file:
			return Response({'error': 'Type et fichier requis'}, status=status.HTTP_400_BAD_REQUEST)
		document = ExportDocument.objects.create(
			export=export,
			document_type=document_type,
			document_file=file,
			uploaded_by=request.user
		)
		serializer = ExportDocumentSerializer(document)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExportDocumentViewSet(viewsets.ModelViewSet):
	queryset = ExportDocument.objects.all()
	serializer_class = ExportDocumentSerializer
	permission_classes = [IsAuthenticated]
