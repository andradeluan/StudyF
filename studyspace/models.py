from django.db import models
from django.contrib.auth.models import User

class CardVideo(models.Model):
    # ID do vídeo como chave primária
    id_video = models.CharField(max_length=100, primary_key=True)

    # Chave estrangeira para o usuário
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')

    # Campos adicionais
    titulo = models.CharField(max_length=200)
    resumo = models.TextField(blank=True, null=True)
    roteiro_estudos = models.TextField(blank=True, null=True)
    flashcards = models.JSONField(blank=True, null=True)  # Armazena flashcards no formato JSON

    # Timestamp para registro de criação/modificação
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo