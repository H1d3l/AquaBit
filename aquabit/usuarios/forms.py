from django import forms

class RegistrarUsuarioForm(forms.Form):
    TIPO_USUARIO = [
        ('Estud.','Estudante'),
        ('Téc.','Técnico'),
        ('Prod.','Produtor'),
    ]
    nome = forms.CharField(required=True)
    email = forms.CharField(required=True)
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    cpf_cnpj = forms.CharField(required=True)
    cidade = forms.CharField(required=True)
    estado = forms.CharField(required=True)
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO)
    uso_aquabit = forms.BooleanField(required=False)


class LoginUsuarioForm(forms.Form):
    cpf_cnpj = forms.CharField(required=True)
    senha = forms.CharField(required=True)




