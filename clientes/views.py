from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ClienteForm
from .models import Cliente


def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, "clientes/listar.html", {
        "clientes": clientes
    })


def cadastrar_cliente(request):
    form = ClienteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cliente cadastrado com sucesso!")
        return redirect("clientes:listar")

    return render(request, "clientes/formulario.html", {
        "form": form
    })
