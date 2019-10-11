from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.base import View
from usuarios.forms import *
from django.contrib.auth.models import User
from usuarios.models import Usuario
import requests,json
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth.base_user import BaseUserManager




# Create your views here.
@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return redirect('login')

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
            #captura os dados e transforma em json
            dados_json = r.json()

            if dados_json['code'] == 200:
                #Verifica se usuario existe no meu banco de dados
                usuario_exist = Usuario.objects.filter(cpf_cnpj=dados_form['cpf_cnpj']).exists()
                if usuario_exist:
                    return redirect('index')
                else:

                    #necessario refatorar a variavel data. Api fornecida esta paginada. Precisa fazer a procura em todos
                    #os links de paginacao.
                    data1 = requests.get('http://teste.aquabit.com.br/api/v1/usuarios/').json()
                    data2 = requests.get("http://teste.aquabit.com.br/api/v1/usuarios/?page=2").json()
                    data_ajustada1 = data1.get('results')
                    data_ajustada2 = data2.get('results')

                    resultado1 = [data for data in data_ajustada1 if data["inscricao_federal"] == dados_form['cpf_cnpj']]
                    resultado2 = [data for data in data_ajustada2 if data["inscricao_federal"] == dados_form['cpf_cnpj']]

                    if resultado1!=[]:
                        for i in data_ajustada1:
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
                        if resultado2!=[]:
                            for i in data_ajustada2:
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
                            return HttpResponse('Usuario não encontrado')
            else:
                return HttpResponse("Acesso negado")
        return render(request, self.template_name, {'form': form})



class ResgistrarUsuarioView(View):
    template_name = 'registrar.html'


    def get(self,request):
        form = RegistrarUsuarioForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = RegistrarUsuarioForm(request.POST)
        data1 = requests.get('http://teste.aquabit.com.br/api/v1/usuarios/').json()
        data2 = requests.get("http://teste.aquabit.com.br/api/v1/usuarios/?page=2").json()
        data_ajustada1 = data1.get('results')
        data_ajustada2 = data2.get('results')



        if form.is_valid():
            dados_form = form.cleaned_data
            resultado1 = [data for data in data_ajustada1 if data["inscricao_federal"] == dados_form['cpf_cnpj']]
            resultado2 = [data for data in data_ajustada2 if data["inscricao_federal"] == dados_form['cpf_cnpj']]

            #Verifica se o usuario esta cadastrada na api
            if resultado1 != []:
                return render(request,'base_usuario.html',{'msg': 'Desculpe. Você já possui um cadastro no Aquabit.',
                                                               'email':dados_form['email']})
            elif resultado2!=[]:
                return render(request,'base_usuario.html',{'msg': 'Desculpe. Você já possui um cadastro no Aquabit.',
                                                               'email':dados_form['email']})
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




class RecuperarSenhaView(View):
    template_name = 'recuperar_senha.html'

    def get(self,request):
        form = RecuperarSenhaForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = RecuperarSenhaForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            cpf_cnpj_usuario = Usuario.objects.get(cpf_cnpj=dados_form['cpf_cnpj'])
            email = cpf_cnpj_usuario.user.email
            usuario = cpf_cnpj_usuario.user
            user = User.objects.get(username=usuario)
            gera_senha = BaseUserManager().make_random_password()
            user.set_password(gera_senha)
            user.save()
            send_email = EmailMessage('Reset senha','A sua nova senha é %s'% gera_senha, to=[email])
            send_email.send()
            enviado = cpf_cnpj_usuario.ocultaemail(email)

            return HttpResponse("A nova senha foi enviada para o email %s" % enviado )

