from django.db import models

from .livro import Livro
from .user import User


class Classificacao(models.Model):

    nota = models.DecimalField(max_digits=4, decimal_places=1, default=0, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="usuarios", null=False)
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="livros", null=False)

    def __str__(self):
        return f"Nota = {self.nota} | Usuario = {self.user} | Livro = {self.livro}"
