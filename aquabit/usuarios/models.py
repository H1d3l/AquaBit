from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    TIPO_USUARIO = [
        ('Estud.','Estudante'),
        ('Téc.','Técnico'),
        ('Prod.','Produtor'),
    ]
    user = models.OneToOneField(User,related_name='usuario',on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=15)
    telefone = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    tipo_usuario =  models.CharField(max_length=20,choices=TIPO_USUARIO)
    uso_aquabit = models.BooleanField(default=False)