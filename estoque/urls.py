from django.urls import path
from . import views

app_name = "estoque"

urlpatterns = [
    path("", views.listar_produtos, name="listar"),
    path("novo/", views.cadastrar_produto, name="cadastrar"),
    path("movimentacao/", views.registrar_movimentacao, name="movimentar"),
]
