from django.contrib import admin

from django.contrib import admin
from .models import CardVideo

@admin.register(CardVideo)
class CardVideoAdmin(admin.ModelAdmin):
    list_display = ('id_video', 'titulo', 'user', 'criado_em', 'atualizado_em')
