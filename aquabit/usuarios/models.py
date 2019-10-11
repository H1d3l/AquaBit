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


    def ocultaemail(self, email):
        count = 0
        fist_part = []
        second_part = []
        third_part = []
        for i in email:
            if i != "@":
                if count<=3:
                    fist_part.append(i)
                    count+=1
                else:
                    second_part.append(i)
            else:
                break
        fist_part = ''.join(fist_part)
        second_part = ''.join(second_part)

        oculto = []
        for k in second_part:
            oculto.append("*")
        count2 = 0
        for j in email:
            count2 += 1
            if count2>len(fist_part+second_part):
                third_part.append(j)

        second_part = "".join(oculto)
        third_part = "".join(third_part)
        email_oculto = fist_part + second_part + third_part

        return email_oculto



