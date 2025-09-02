from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import ItemServico


@admin.register(ItemServico)
class ItemServicoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'descricao', 'quantidade', 'preco_unitario', 'valor_total'
    )
    list_filter = (
        'quantidade',
    )
    search_fields = (
        'nome', 'descricao'
    )


