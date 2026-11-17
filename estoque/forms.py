from django import forms
from .models import Produto, MovimentacaoEstoque


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome",
            "categoria",
            "quantidade",
            "estoque_minimo",
        ]

        labels = {
            "nome": "Nome do produto",
            "categoria": "Categoria",
            "quantidade": "Quantidade inicial",
            "estoque_minimo": "Estoque mínimo",
        }

        help_texts = {
            "nome": "Informe o nome da peça ou do pneu.",
            "categoria": "Selecione o tipo de produto.",
            "quantidade": "Informe quantas unidades estão disponíveis.",
            "estoque_minimo": "O sistema indicará quando o estoque atingir este limite.",
        }

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Pneu aro 15"
            }),
            "categoria": forms.Select(attrs={
                "class": "form-select"
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),
            "estoque_minimo": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0"
            }),
        }


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ["produto", "tipo", "quantidade", "observacao"]

        labels = {
            "produto": "Produto",
            "tipo": "Tipo de movimentação",
            "quantidade": "Quantidade",
            "observacao": "Observação (opcional)",
        }

        help_texts = {
            "produto": "Selecione o produto que será movimentado.",
            "tipo": "Escolha entrada para adicionar ou saída para retirar unidades.",
            "quantidade": "Informe a quantidade de unidades movimentadas.",
            "observacao": "Registre um detalhe, se necessário.",
        }

        widgets = {
            "produto": forms.Select(attrs={
                "class": "form-select"
            }),
            "tipo": forms.Select(attrs={
                "class": "form-select"
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1"
            }),
            "observacao": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Reposição de estoque"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["produto"].queryset = Produto.objects.filter(
            ativo=True
        )

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade <= 0:
            raise forms.ValidationError(
                "A quantidade deve ser maior que zero."
            )
        return quantidade
