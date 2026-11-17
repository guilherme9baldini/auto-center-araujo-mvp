from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "telefone", "veiculo"]

        labels = {
            "nome": "Nome completo",
            "telefone": "Telefone para contato",
            "veiculo": "Veículo do cliente (opcional)",
        }

        help_texts = {
            "nome": "Digite o nome do cliente.",
            "telefone": "Informe um telefone com DDD.",
            "veiculo": "Informe o modelo do veículo, se souber.",
        }

        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: João da Silva"
            }),
            "telefone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "(11) 99999-9999"
            }),
            "veiculo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Honda Civic"
            }),
        }

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if not nome:
            raise forms.ValidationError("Informe o nome do cliente.")
        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data["telefone"].strip()
        if not telefone:
            raise forms.ValidationError("Informe o telefone.")
        return telefone
