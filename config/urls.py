from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import health_check

urlpatterns = [
    path("", lambda request: redirect("estoque:listar")),
    path("health/", health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("clientes/", include("clientes.urls")),
    path("estoque/", include("estoque.urls")),
]
