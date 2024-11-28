from django.db import transaction

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=True, methods=["post", "get"])
    def finalizar(self, request, pk=None):
        compra = self.get_object()

        if compra.status != Compra.StatusCompra.CARRINHO:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"status": "Compra já finalizada"},
            )

        with transaction.atomic():
            for item in compra.itens.all():

                if item.quantidade > item.livro.quantidade:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={
                            "status": "Quantidade insuficiente",
                            "livro": item.livro.titulo,
                            "quantidade_disponivel": item.livro.quantidade,
                        },
                    )

                item.livro.quantidade -= item.quantidade
                item.livro.save()

            compra.status = Compra.StatusCompra.FINALIZADO
            compra.save()

        return Response(status=status.HTTP_200_OK, data={"status": "Compra finalizada"})
