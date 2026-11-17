from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Q


class Produto(models.Model):
    class Categoria(models.TextChoices):
        PNEU = "PNEU", "Pneu"
        PECA = "PECA", "Peça"
        OUTRO = "OUTRO", "Outro"

    nome = models.CharField(max_length=150)
    categoria = models.CharField(
        max_length=10,
        choices=Categoria.choices,
        default=Categoria.OUTRO
    )
    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
