from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import PessoaFalecida


@admin.register(PessoaFalecida)
class PessoaFalecidaAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'data_nascimento', 'data_falecimento', 'familia', 'documento_cpf_rg'
    )
    list_filter = (
        'data_falecimento', 'familia'
    )
    search_fields = (
        'nome', 'documento_cpf_rg', 'causa_obito', 'local_obito'
    )
    date_hierarchy = 'data_falecimento'


