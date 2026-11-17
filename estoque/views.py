from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from .forms import ProdutoForm, MovimentacaoForm
from .models import Produto, MovimentacaoEstoque


def listar_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, "estoque/listar.html", {
        "produtos": produtos
    })


def cadastrar_produto(request):
    form = ProdutoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            produto = form.save()
            if produto.quantidade > 0:
                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo=MovimentacaoEstoque.Tipo.ENTRADA,
                    quantidade=produto.quantidade,
                    observacao="Estoque inicial"
                )

        messages.success(request, "Produto cadastrado com sucesso!")
        return redirect("estoque:listar")

    return render(request, "estoque/formulario.html", {
        "form": form
    })


def registrar_movimentacao(request):
    form = MovimentacaoForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        dados = form.cleaned_data

        try:
            with transaction.atomic():
                produto = Produto.objects.select_for_update().get(
                    pk=dados["produto"].pk,
                    ativo=True
                )

                quantidade = dados["quantidade"]
                tipo = dados["tipo"]

                if tipo == MovimentacaoEstoque.Tipo.SAIDA:
                    if quantidade > produto.quantidade:
                        form.add_error(
                            "quantidade",
                            "A saída não pode ser maior que o estoque disponível."
                        )
                        raise ValueError("Estoque insuficiente.")

                    produto.quantidade -= quantidade
                else:
                    produto.quantidade += quantidade

                produto.save(update_fields=["quantidade"])

                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo=tipo,
                    quantidade=quantidade,
                    observacao=dados["observacao"]
                )

            messages.success(request, "Movimentação registrada com sucesso!")
            return redirect("estoque:listar")

        except ValueError:
            pass
        except Produto.DoesNotExist:
            form.add_error("produto", "Produto não encontrado ou inativo.")

    return render(request, "estoque/movimentacao.html", {
        "form": form
    })
