from .user import UserSerializer
from .categoria import CategoriaSerializer
from .editora import EditoraSerializer
from .autor import AutorSerializer
from .livro import LivroSerializer, LivroListSerializer, LivroRetrieveSerializer
from .compra import (
    CompraSerializer,
    CompraCreateUpdateSerializer,
    ItensCompraListSerializer,
    ItensCompraSerializer,
    CompraListSerializer,
)
