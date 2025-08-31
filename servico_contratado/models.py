from django.db import models
from pessoa_falecida.models import PessoaFalecida
from item_servico.models import ItemServico


class ServicoContratado(models.Model):
    """Modelo para representar serviços contratados para uma pessoa falecida."""
    
    pessoa_falecida = models.ForeignKey(
        PessoaFalecida,
        on_delete=models.CASCADE,
        verbose_name="Pessoa Falecida",
        related_name="servicos_contratados"
    )
    item_servico = models.ForeignKey(
        ItemServico,
        on_delete=models.CASCADE,
        verbose_name="Item de Serviço"
    )
    descricao_adicional = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição Adicional"
    )
    valor_final = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor Final"
    )
    
    class Meta:
        verbose_name = "Serviço Contratado"
        verbose_name_plural = "Serviços Contratados"
        ordering = ['pessoa_falecida', 'item_servico']
    
    def __str__(self):
        return f"{self.pessoa_falecida.nome} - {self.item_servico.nome}"
