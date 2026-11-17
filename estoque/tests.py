from django.test import TestCase
from django.urls import reverse

from .models import Produto, MovimentacaoEstoque


class EstoqueTests(TestCase):

    def setUp(self):
        self.produto = Produto.objects.create(
            nome="Pneu Aro 15",
            categoria=Produto.Categoria.PNEU,
            quantidade=10,
            estoque_minimo=3
        )

    def test_listar_produtos(self):
        response = self.client.get(reverse("estoque:listar"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pneu Aro 15")

    def test_alerta_estoque_baixo(self):
        self.produto.quantidade = 2
        self.produto.save()

        self.assertTrue(self.produto.estoque_baixo)

    def test_registrar_entrada(self):
        response = self.client.post(
            reverse("estoque:movimentar"),
            {
                "produto": self.produto.pk,
                "tipo": "ENTRADA",
                "quantidade": 5,
                "observacao": "Reposição",
            }
        )

        self.assertRedirects(response, reverse("estoque:listar"))

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 15)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 1)

    def test_registrar_saida(self):
        response = self.client.post(
            reverse("estoque:movimentar"),
            {
                "produto": self.produto.pk,
                "tipo": "SAIDA",
                "quantidade": 4,
                "observacao": "Venda",
            }
        )

        self.assertRedirects(response, reverse("estoque:listar"))

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 6)

    def test_impedir_saida_maior_que_estoque(self):
        response = self.client.post(
            reverse("estoque:movimentar"),
            {
                "produto": self.produto.pk,
                "tipo": "SAIDA",
                "quantidade": 15,
                "observacao": "Teste",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 10)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 0)

    def test_impedir_quantidade_zero(self):
        response = self.client.post(
            reverse("estoque:movimentar"),
            {
                "produto": self.produto.pk,
                "tipo": "ENTRADA",
                "quantidade": 0,
                "observacao": "Teste",
            }
        )

        self.assertEqual(response.status_code, 200)

        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade, 10)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 0)
