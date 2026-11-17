from django.test import TestCase
from django.urls import reverse

from .models import Cliente


class ClienteTests(TestCase):

    def test_cadastrar_cliente(self):
        response = self.client.post(
            reverse("clientes:cadastrar"),
            {
                "nome": "João da Silva",
                "telefone": "(11) 99999-9999",
                "veiculo": "Honda Civic",
            }
        )

        self.assertRedirects(response, reverse("clientes:listar"))
        self.assertTrue(
            Cliente.objects.filter(nome="João da Silva").exists()
        )

    def test_nao_cadastrar_cliente_sem_nome(self):
        response = self.client.post(
            reverse("clientes:cadastrar"),
            {
                "nome": "",
                "telefone": "(11) 99999-9999",
                "veiculo": "Honda Civic",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 0)

    def test_listar_clientes(self):
        Cliente.objects.create(
            nome="Maria",
            telefone="11988887777"
        )

        response = self.client.get(reverse("clientes:listar"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Maria")
