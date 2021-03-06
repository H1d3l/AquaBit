"""aquabit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as v
from django.urls import path
from usuarios.views import *
from usuarios import views as usuarioview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',usuarioview.index,name='index'),
    path('registrar/',ResgistrarUsuarioView.as_view(),name='registrar'),
    path('login/',v.LoginView.as_view(template_name='login.html'),name='login'),
    path('login_user_aquabit/',LoginUsuarioAquabitView.as_view(template_name='login_usuario_aquabit.html'),
         name='login_aquabit'),
    path('logout/',v.LogoutView.as_view(template_name='logout.html')),
    path('resetsenha/', RecuperarSenhaView.as_view(), name='resetsenha'),
]
