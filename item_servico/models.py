from django.db import models


class ItemServico(models.Model):
    """Modelo para representar itens de serviço disponíveis."""
    
    nome = models.CharField(max_length=200, verbose_name="Nome")
    descricao = models.TextField(verbose_name="Descrição")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    preco_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Preço Unitário"
    )
    imagem = models.ImageField(
        upload_to='itens_servicos/',
        blank=True,
        null=True,
        verbose_name="Imagem",
        help_text="Imagem do item/serviço"
    )
    
    class Meta:
        verbose_name = "Item de Serviço"
        verbose_name_plural = "Itens de Serviço"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco_unitario}"
    
    @property
    def valor_total(self):
        """Calcula o valor total do item (quantidade * preço unitário)."""
        return self.quantidade * self.preco_unitario
