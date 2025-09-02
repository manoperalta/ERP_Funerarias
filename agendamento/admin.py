from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = (
        'pessoa_falecida', 'funcionario', 'data_agendamento', 
        'hora_agendamento', 'local_velorio', 'local_sepultamento', 
        'data_sepultamento'
    )
    list_filter = (
        'data_agendamento', 'funcionario__cargo', 'local_velorio', 
        'local_sepultamento'
    )
    search_fields = (
        'pessoa_falecida__nome', 'funcionario__first_name', 
        'funcionario__last_name', 'local_velorio', 'local_sepultamento'
    )
    date_hierarchy = 'data_agendamento'
    ordering = ('-data_agendamento',)


