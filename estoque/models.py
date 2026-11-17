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

    class Meta:
        ordering = ["nome"]
        constraints = [
            models.CheckConstraint(
                condition=Q(quantidade__gte=0),
                name="produto_quantidade_nao_negativa"
            ),
            models.CheckConstraint(
                condition=Q(estoque_minimo__gte=0),
                name="produto_estoque_minimo_nao_negativo"
            ),
        ]

    def __str__(self):
        return self.nome

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo


class MovimentacaoEstoque(models.Model):

    class Tipo(models.TextChoices):
        ENTRADA = "ENTRADA", "Entrada"
        SAIDA = "SAIDA", "Saída"

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name="movimentacoes"
    )

    tipo = models.CharField(
        max_length=10,
        choices=Tipo.choices
    )

    quantidade = models.PositiveIntegerField()
    observacao = models.CharField(max_length=255, blank=True)
    data_movimentacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data_movimentacao"]
        constraints = [
            models.CheckConstraint(
                condition=Q(quantidade__gt=0),
                name="movimentacao_quantidade_positiva"
            ),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome}"
