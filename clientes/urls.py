from django.urls import path
from . import views

app_name = "clientes"

urlpatterns = [
    path("", views.listar_clientes, name="listar"),
    path("novo/", views.cadastrar_cliente, name="cadastrar"),
]
