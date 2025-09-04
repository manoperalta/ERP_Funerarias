from django.db import models
from django.utils import timezone
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
    
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('transferencia', 'Transferência Bancária'),
        ('boleto', 'Boleto Bancário'),
    ]
    
    pessoa_falecida = models.ForeignKey(
        PessoaFalecida,
        on_delete=models.CASCADE,
        verbose_name="Pessoa Falecida",
        related_name="financeiros"
    )
    servico_contratado = models.ForeignKey(
        'servico_contratado.ServicoContratado',
        on_delete=models.CASCADE,
        verbose_name="Serviço Contratado",
        related_name="registros_financeiros",
        blank=True,
        null=True
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
    data_pagamento = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data do Pagamento"
    )
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMA_PAGAMENTO_CHOICES,
        blank=True,
        null=True,
        verbose_name="Forma de Pagamento"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pendente',
        verbose_name="Status"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    data_criacao = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Financeiro"
        verbose_name_plural = "Financeiros"
        ordering = ['-data_vencimento', '-data_criacao']
    
    def __str__(self):
        return f"{self.pessoa_falecida.nome} - {self.tipo} - R$ {self.valor}"
    
    def marcar_como_pago(self, forma_pagamento=None):
        """Marca o registro como pago."""
        self.status = 'pago'
        self.data_pagamento = timezone.now()
        if forma_pagamento:
            self.forma_pagamento = forma_pagamento
        self.save()
    
    @property
    def tem_nota_fiscal(self):
        """Verifica se existe nota fiscal associada."""
        return self.servico_contratado and self.servico_contratado.pdf_nota_fiscal
    
    @property
    def numero_nota_fiscal(self):
        """Retorna o número da nota fiscal se existir."""
        if self.servico_contratado:
            return self.servico_contratado.numero_nota_fiscal
        return None
