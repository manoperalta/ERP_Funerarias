from django.db import models
from django.utils import timezone
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
    data_contratacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data da Contratação"
    )
    numero_nota_fiscal = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Número da Nota Fiscal"
    )
    
    class Meta:
        verbose_name = "Serviço Contratado"
        verbose_name_plural = "Serviços Contratados"
        ordering = ['-data_contratacao', 'pessoa_falecida', 'item_servico']
    
    def __str__(self):
        return f"{self.pessoa_falecida.nome} - {self.item_servico.nome}"
    
    def gerar_numero_nota_fiscal(self):
        """Gera um número único para a nota fiscal."""
        if not self.numero_nota_fiscal:
            # Formato: NF + ano + mês + dia + ID do serviço
            data = self.data_contratacao
            self.numero_nota_fiscal = f"NF{data.year}{data.month:02d}{data.day:02d}{self.pk:04d}"
            self.save()
        return self.numero_nota_fiscal
