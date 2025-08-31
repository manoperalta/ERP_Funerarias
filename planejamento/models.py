from django.db import models
from pessoa_falecida.models import PessoaFalecida


class Planejamento(models.Model):
    """Modelo para representar planejamento de serviços funerários."""
    
    pessoa_falecida = models.OneToOneField(
        PessoaFalecida,
        on_delete=models.CASCADE,
        verbose_name="Pessoa Falecida",
        related_name="planejamento"
    )
    nome_plano = models.CharField(max_length=200, verbose_name="Nome do Plano")
    descricao = models.TextField(verbose_name="Descrição")
    valor_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor Total"
    )
    
    class Meta:
        verbose_name = "Planejamento"
        verbose_name_plural = "Planejamentos"
        ordering = ['nome_plano']
    
    def __str__(self):
        return f"{self.nome_plano} - {self.pessoa_falecida.nome}"
