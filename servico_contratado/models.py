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
    descricao_adicional = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição Adicional"
    )
    taxa_imposto = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        verbose_name="Taxa de Imposto (%)",
        help_text="Taxa de imposto em porcentagem (padrão: 10%)"
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
    pdf_nota_fiscal = models.FileField(
        upload_to='notas_fiscais/',
        blank=True,
        null=True,
        verbose_name="PDF da Nota Fiscal"
    )
    
    class Meta:
        verbose_name = "Serviço Contratado"
        verbose_name_plural = "Serviços Contratados"
        ordering = ['-data_contratacao', 'pessoa_falecida']
    
    def __str__(self):
        return f"{self.pessoa_falecida.nome} - {self.data_contratacao.strftime('%d/%m/%Y')}"
    
    @property
    def subtotal(self):
        """Calcula o subtotal de todos os itens do contrato."""
        return sum(item.valor_total for item in self.itens.all())
    
    @property
    def valor_imposto(self):
        """Calcula o valor do imposto."""
        return (self.subtotal * self.taxa_imposto) / 100
    
    @property
    def valor_total(self):
        """Calcula o valor total incluindo impostos."""
        return self.subtotal + self.valor_imposto
    
    def gerar_numero_nota_fiscal(self):
        """Gera um número único para a nota fiscal."""
        if not self.numero_nota_fiscal:
            # Formato: NF + ano + mês + dia + ID do serviço
            data = self.data_contratacao
            self.numero_nota_fiscal = f"NF{data.year}{data.month:02d}{data.day:02d}{self.pk:04d}"
            self.save()
        return self.numero_nota_fiscal


class ItemServicoContratado(models.Model):
    """Modelo para representar itens individuais de um serviço contratado."""
    
    servico_contratado = models.ForeignKey(
        ServicoContratado,
        on_delete=models.CASCADE,
        related_name="itens",
        verbose_name="Serviço Contratado"
    )
    item_servico = models.ForeignKey(
        ItemServico,
        on_delete=models.CASCADE,
        verbose_name="Item de Serviço"
    )
    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade"
    )
    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Unitário"
    )
    
    class Meta:
        verbose_name = "Item do Serviço Contratado"
        verbose_name_plural = "Itens dos Serviços Contratados"
        unique_together = ['servico_contratado', 'item_servico']
    
    def __str__(self):
        return f"{self.item_servico.nome} - Qtd: {self.quantidade}"
    
    @property
    def valor_total(self):
        """Calcula o valor total do item (quantidade * valor unitário)."""
        return self.quantidade * self.valor_unitario
    
    def save(self, *args, **kwargs):
        """Sobrescreve o save para definir o valor unitário automaticamente."""
        if not self.valor_unitario:
            self.valor_unitario = self.item_servico.preco_unitario
        super().save(*args, **kwargs)

