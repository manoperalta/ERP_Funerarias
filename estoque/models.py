from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class CategoriaEstoque(models.Model):
    """Categorias para organizar produtos do estoque."""
    
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nome da Categoria"
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    
    cor = models.CharField(
        max_length=7,
        default="#6c757d",
        verbose_name="Cor da Categoria",
        help_text="Cor para identificação visual (formato: #000000)"
    )
    
    ativa = models.BooleanField(
        default=True,
        verbose_name="Categoria Ativa"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    class Meta:
        verbose_name = "Categoria de Estoque"
        verbose_name_plural = "Categorias de Estoque"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class ProdutoEstoque(models.Model):
    """Produtos controlados no estoque."""
    
    UNIDADE_CHOICES = [
        ('un', 'Unidade'),
        ('kg', 'Quilograma'),
        ('g', 'Grama'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        ('m', 'Metro'),
        ('cm', 'Centímetro'),
        ('m2', 'Metro Quadrado'),
        ('m3', 'Metro Cúbico'),
        ('cx', 'Caixa'),
        ('pct', 'Pacote'),
        ('dz', 'Dúzia'),
    ]
    
    codigo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código do Produto",
        help_text="Código único para identificação"
    )
    
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Produto"
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    
    categoria = models.ForeignKey(
        CategoriaEstoque,
        on_delete=models.PROTECT,
        verbose_name="Categoria"
    )
    
    unidade_medida = models.CharField(
        max_length=5,
        choices=UNIDADE_CHOICES,
        default='un',
        verbose_name="Unidade de Medida"
    )
    
    preco_custo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço de Custo"
    )
    
    preco_venda = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço de Venda"
    )
    
    quantidade_atual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Quantidade Atual"
    )
    
    quantidade_minima = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Quantidade Mínima",
        help_text="Quantidade mínima para alerta de estoque baixo"
    )
    
    quantidade_maxima = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Quantidade Máxima",
        help_text="Quantidade máxima recomendada"
    )
    
    localizacao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Localização",
        help_text="Local onde o produto está armazenado"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Produto Ativo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    
    class Meta:
        verbose_name = "Produto de Estoque"
        verbose_name_plural = "Produtos de Estoque"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    @property
    def valor_total_estoque(self):
        """Calcula o valor total do estoque atual."""
        return self.quantidade_atual * self.preco_custo
    
    @property
    def estoque_baixo(self):
        """Verifica se o estoque está baixo."""
        return self.quantidade_atual <= self.quantidade_minima
    
    @property
    def estoque_alto(self):
        """Verifica se o estoque está alto."""
        if self.quantidade_maxima:
            return self.quantidade_atual >= self.quantidade_maxima
        return False
    
    @property
    def margem_lucro(self):
        """Calcula a margem de lucro em percentual."""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0


class MovimentacaoEstoque(models.Model):
    """Registro de movimentações de entrada e saída do estoque."""
    
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
        ('perda', 'Perda'),
        ('transferencia', 'Transferência'),
    ]
    
    produto = models.ForeignKey(
        ProdutoEstoque,
        on_delete=models.PROTECT,
        verbose_name="Produto"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Movimentação"
    )
    
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Quantidade"
    )
    
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço Unitário"
    )
    
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )
    
    documento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Número do Documento",
        help_text="Nota fiscal, recibo, etc."
    )
    
    fornecedor = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Fornecedor/Cliente"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Usuário Responsável"
    )
    
    data_movimentacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Movimentação"
    )
    
    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} - {self.quantidade}"
    
    @property
    def valor_total(self):
        """Calcula o valor total da movimentação."""
        return self.quantidade * self.preco_unitario
    
    def save(self, *args, **kwargs):
        """Atualiza o estoque do produto após a movimentação."""
        is_new = self.pk is None
        
        if is_new:
            # Nova movimentação - atualiza estoque
            if self.tipo in ['entrada', 'ajuste']:
                self.produto.quantidade_atual += self.quantidade
            elif self.tipo in ['saida', 'perda']:
                self.produto.quantidade_atual -= self.quantidade
            
            self.produto.save()
        
        super().save(*args, **kwargs)


class AlertaEstoque(models.Model):
    """Alertas automáticos para controle de estoque."""
    
    TIPO_ALERTA_CHOICES = [
        ('estoque_baixo', 'Estoque Baixo'),
        ('estoque_alto', 'Estoque Alto'),
        ('produto_zerado', 'Produto Zerado'),
        ('vencimento', 'Próximo ao Vencimento'),
    ]
    
    produto = models.ForeignKey(
        ProdutoEstoque,
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )
    
    tipo_alerta = models.CharField(
        max_length=20,
        choices=TIPO_ALERTA_CHOICES,
        verbose_name="Tipo de Alerta"
    )
    
    mensagem = models.TextField(
        verbose_name="Mensagem do Alerta"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Alerta Ativo"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_resolucao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data de Resolução"
    )
    
    class Meta:
        verbose_name = "Alerta de Estoque"
        verbose_name_plural = "Alertas de Estoque"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.get_tipo_alerta_display()} - {self.produto.nome}"
