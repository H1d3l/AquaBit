from django.shortcuts import render,redirect
from django.views.generic.base import View
from usuarios.forms import *
from django.contrib.auth.models import User
import requests,json
# Create your views here.

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
                user = User.objects.create(username=dados_form['nome'],
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
                return redirect('registrar')
        return render(request,self.template_name,{'form':form})

