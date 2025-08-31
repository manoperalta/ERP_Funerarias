from django.db import models
from funcionario.models import Funcionario
from pessoa_falecida.models import PessoaFalecida


class Agendamento(models.Model):
    """Modelo para representar agendamentos de serviços funerários."""
    
    pessoa_falecida = models.ForeignKey(
        PessoaFalecida,
        on_delete=models.CASCADE,
        verbose_name="Pessoa Falecida",
        related_name="agendamentos"
    )
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE,
        verbose_name="Funcionário Responsável"
    )
    data_agendamento = models.DateTimeField(verbose_name="Data do Agendamento")
    hora_agendamento = models.TimeField(verbose_name="Hora do Agendamento")
    local_velorio = models.CharField(max_length=200, verbose_name="Local do Velório")
    local_sepultamento = models.CharField(max_length=200, verbose_name="Local do Sepultamento")
    data_sepultamento = models.DateTimeField(verbose_name="Data do Sepultamento")
    
    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['-data_agendamento']
    
    def __str__(self):
        return f"{self.pessoa_falecida.nome} - {self.data_agendamento.strftime('%d/%m/%Y %H:%M')}"
