from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers import CompraCreateUpdateSerializer, CompraListSerializer, CompraSerializer


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_anonymous:
            raise PermissionDenied("Você precisa estar autenticado para acessar este recurso.")
        # Se o usuário for superusuário, retorna todas as compras
        if usuario.is_superuser:
            return Compra.objects.all()
        # Verifica se o usuário pertence ao grupo "Administradores"
        if usuario.groups.filter(name="Administradores").exists():
            return Compra.objects.all()
        # Caso contrário, retorna apenas as compras do usuário logado
        return Compra.objects.filter(usuario=usuario)

    def get_serializer_class(self):
        if self.action == "list":
            return CompraListSerializer
        if self.action in ("create", "update"):
            return CompraCreateUpdateSerializer
        return CompraSerializer
