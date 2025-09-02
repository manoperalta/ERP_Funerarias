from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Financeiro


@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display = (
        'pessoa_falecida', 'tipo', 'descricao', 'valor', 'data_vencimento', 'status'
    )
    list_filter = (
        'tipo', 'status', 'data_vencimento'
    )
    search_fields = (
        'pessoa_falecida__nome', 'descricao'
    )
    date_hierarchy = 'data_vencimento'


