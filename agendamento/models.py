from django.db import models
from django.contrib.auth.models import User  # Importa o modelo de usuário padrão do Django


class Instrumento(models.Model):
    id= models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Professor(models.Model):
    id= models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento 1:1 com User
    instrumentos = models.ManyToManyField(Instrumento)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Aluno(models.Model):
    matricula = models.AutoField(primary_key=True) 
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento 1:1 com User
    instrumento_interesse = models.ForeignKey(Instrumento, on_delete=models.SET_NULL, null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


class Disponibilidade(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    dia_semana = models.IntegerField(choices=[(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo')])
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    def __str__(self):
        return f"{self.professor} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fim}"


class Agendamento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    duracao = models.IntegerField(default=60)  # Duração em minutos
    cancelado = models.BooleanField(default=False)

    def __str__(self):
        return f"Aula de {self.instrumento} com {self.professor} para {self.aluno} em {self.data_hora}"