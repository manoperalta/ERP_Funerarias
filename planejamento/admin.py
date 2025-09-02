from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Planejamento


@admin.register(Planejamento)
class PlanejamentoAdmin(admin.ModelAdmin):
    list_display = (
        'pessoa_falecida', 'nome_plano', 'valor_total'
    )
    search_fields = (
        'pessoa_falecida__nome', 'nome_plano', 'descricao'
    )
    


