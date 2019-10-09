from django.shortcuts import render,redirect
from django.views.generic.base import View
from usuarios.forms import *
from django.contrib.auth.models import User
from usuarios.models import Usuario
import requests,json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


# Create your views here.
@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return render(request, 'erros.html', {'msg': 'Acesso negado'})


class LoginUsuarioAquabitView(View):
    template_name = 'login_usuario_aquabit.html'


    def get(self,request):
        form = LoginUsuarioForm()

        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = LoginUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            r = requests.post('http://teste.aquabit.com.br/api/v1/auth/login/',
                              json={ "inscricao_federal":dados_form['cpf_cnpj'],"senha":dados_form['senha']})


            if r.status_code == 200:
                data = requests.get("http://teste.aquabit.com.br/api/v1/usuarios/?page=2").json()
                data_ajustada = data.get('results')

                for i in data_ajustada:
                    if dados_form["cpf_cnpj"] == i["inscricao_federal"]:
                       for k in i['propriedades']:
                            user = User.objects.create_user(username=i['nome'],
                                                            email=i['email'],
                                                            password=dados_form['senha'])

                            usuario = Usuario(nome=i['nome'],
                                              telefone=i['telefone'],
                                              cpf_cnpj=i['inscricao_federal'],
                                              cidade=k['cidade'],
                                              estado=k['estado'],
                                              tipo_usuario=i['tipo_de_usuario']['nome'],
                                              uso_aquabit=True,
                                              user=user)
                            usuario.save()
                            return redirect('index')


            else:
                return render(request,'erros.html',{'msg':'Acesso negado'})


class ResgistrarUsuarioView(View):
    template_name = 'registrar.html'

    def get(self,request):
        form = RegistrarUsuarioForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = RegistrarUsuarioForm(request.POST)
        data = requests.get("http://teste.aquabit.com.br/api/v1/usuarios/").json()
        if form.is_valid():
            dados_form = form.cleaned_data

            for i in data['results']:
                if dados_form["cpf_cnpj"] == i["inscricao_federal"]:
                    return render(request,'base_usuario.html',{'msg': 'Desculpe. Você já possui um cadastro no Aquabit.'})

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
                                      uso_aquabit=False,
                                      user=user)
                    usuario.save()
                    return redirect('login')
        return render(request,self.template_name,{'form':form})

