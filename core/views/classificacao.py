from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from core.models import Classificacao
from core.serializers import ClassificacaoSerializer


class ClassificacaoViewSet(ModelViewSet):
    queryset = Classificacao.objects.all()
    serializer_class = ClassificacaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["nota"]
    search_fields = ["nota"]
    ordering_fields = ["nota"]
    ordering = ["nota"]
