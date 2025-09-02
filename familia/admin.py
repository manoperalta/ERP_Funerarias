from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Familia


@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = (
        'nome_responsavel', 'grau_parentesco', 'telefone', 'email', 'endereco'
    )
    list_filter = (
        'grau_parentesco',
    )
    search_fields = (
        'nome_responsavel', 'telefone', 'email', 'endereco'
    )


