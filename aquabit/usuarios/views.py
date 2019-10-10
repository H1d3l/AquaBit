from django.shortcuts import render,redirect
from django.views.generic.base import View
from usuarios.forms import *
from django.contrib.auth.models import User
from usuarios.models import Usuario
import requests
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    return render(request,'index.html')



class ResgistrarUsuarioView(View):
    template_name = 'registrar.html'

    def get(self,request):
        form = RegistrarUsuarioForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = RegistrarUsuarioForm(request.POST)
        data = requests.get("http://teste.aquabit.com.br/api/v1/usuarios/").text
        if form.is_valid():
            dados_form = form.cleaned_data
            if dados_form["cpf_cnpj"] in data:
                return render(request,'base_usuario.html',{'msg': 'Erro! Já existe um usuário com o mesmo cnpj'})
            else:
                user = User.objects.create_user(username=dados_form['nome'],
                                           email=dados_form['email'],
                                           password=dados_form['senha'])

                usuario = Usuario(nome=dados_form['nome'],
                                  telefone=dados_form['telefone'],
                                  cpf_cnpj=dados_form['cpf_cnpj'],
                                  cidade=dados_form['cidade'],
                                  estado=dados_form['estado'],
                                  tipo_usuario=dados_form['tipo_usuario'],
                                  uso_aquabit=dados_form['uso_aquabit'],
                                  user=user)
                usuario.save()
                return redirect('login')
        return render(request,self.template_name,{'form':form})

