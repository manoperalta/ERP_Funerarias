from django.db import models
from pessoa_falecida.models import PessoaFalecida


class Financeiro(models.Model):
    """Modelo para representar informações financeiras dos serviços."""
    
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]
    
    pessoa_falecida = models.ForeignKey(
        PessoaFalecida,
        on_delete=models.CASCADE,
        verbose_name="Pessoa Falecida",
        related_name="financeiros"
    )
    tipo = models.CharField(
        max_length=10, 
        choices=TIPO_CHOICES, 
        verbose_name="Tipo"
    )
    descricao = models.TextField(verbose_name="Descrição")
    valor = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Valor"
    )
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pendente',
        verbose_name="Status"
    )
    
    class Meta:
        verbose_name = "Financeiro"
        verbose_name_plural = "Financeiros"
        ordering = ['-data_vencimento']
    
    def __str__(self):
        return f"{self.pessoa_falecida.nome} - {self.tipo} - R$ {self.valor}"
