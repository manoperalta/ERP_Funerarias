from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'cargo', 'telefone', 'email'
    )
    list_filter = (
        'cargo',
    )
    search_fields = (
        'nome', 'email', 'telefone'
    )


