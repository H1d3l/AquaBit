from django import forms
from django.contrib.auth.models import User
from usuarios.models import *
from django.forms.utils import ErrorDict, ErrorList, pretty_name

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

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS,
                            forms.utils.ErrorList())

        errors.append(message)

    #Verifica se o usuario esta cadastrado no BD
    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['nome']).exists()
        cpf_cnpj_exists = Usuario.objects.filter(cpf_cnpj=self.cleaned_data['cpf_cnpj']).exists()

        if user_exists and cpf_cnpj_exists:
            self.adiciona_erro('Já existe um cadastro no Aquabit')
            valid = False

        return valid



class LoginUsuarioForm(forms.Form):
    cpf_cnpj = forms.CharField(required=True)
    senha = forms.CharField(required=True)




