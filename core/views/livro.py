from django.db.models.aggregates import Sum
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from core.models import Livro
from core.serializers import (
    LivroAlterarPrecoSerializer,
    LivroListSerializer,
    LivroRetrieveSerializer,
    LivroSerializer,
    LivroAjustarEstoqueSerializer,
)


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["categoria__descricao", "editora__nome"]
    search_fields = ["titulo"]
    ordering_fields = ["titulo", "preco"]
    ordering = ["titulo"]

    def get_serializer_class(self):
        if self.action == "list":
            return LivroListSerializer
        elif self.action == "retrieve":
            return LivroRetrieveSerializer
        return LivroSerializer

    @action(detail=True, methods=["patch"])
    def alterar_preco(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        livro.preco = serializer.validated_data["preco"]
        livro.save()

        return Response(
            {"detail": f"Preço do livro '{livro.titulo}' atualizado para {livro.preco}."}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def ajustar_estoque(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAjustarEstoqueSerializer(data=request.data, context={"livro": livro})
        serializer.is_valid(raise_exception=True)

        quantidade_ajuste = serializer.validated_data["quantidade"]

        livro.quantidade += quantidade_ajuste
        livro.save()

        return Response(
            {"status": "Quantidade ajustada com sucesso", "novo_estoque": livro.quantidade}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["get"])
    def mais_vendidos(self, request):
        # Otimizando a consulta com select_related, caso haja relação ForeignKey
        livros = (
            Livro.objects.annotate(total_vendidos=Sum("itens_compra__quantidade"))
            .filter(total_vendidos__gt=10)
            .order_by("-total_vendidos")
        )  # Ordena pelo total vendido em ordem decrescente

        # Verificando se há livros e formatando os dados
        if livros.exists():
            data = [
                {
                    "id": livro.id,
                    "titulo": livro.titulo,
                    "total_vendidos": livro.total_vendidos,
                }
                for livro in livros
            ]
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Nenhum livro encontrado com mais de 10 vendas."},
                status=status.HTTP_404_NOT_FOUND,
            )
