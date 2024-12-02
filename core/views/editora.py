from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from core.models import Editora
from core.serializers import EditoraSerializer


class EditoraViewSet(ModelViewSet):
    queryset = Editora.objects.all()
    serializer_class = EditoraSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["nome", "email", "cidade"]
    search_fields = ["site"]
    ordering_fields = ["nome", "email", "cidade"]
    ordering = ["nome"]
