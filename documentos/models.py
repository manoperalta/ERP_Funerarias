from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from pessoa_falecida.models import PessoaFalecida
from familia.models import Familia
from servico_contratado.models import ServicoContratado
import uuid

User = get_user_model()


class TemplateDocumento(models.Model):
    """Templates para geração de documentos."""
    
    TIPO_CHOICES = [
        ('contrato', 'Contrato de Serviços'),
        ('certidao', 'Certidão de Óbito'),
        ('memorial', 'Memorial'),
        ('orcamento', 'Orçamento'),
        ('recibo', 'Recibo'),
        ('declaracao', 'Declaração'),
        ('compartilhamento', 'Página de Compartilhamento'),
    ]
    
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome do Template"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Documento"
    )
    
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    
    conteudo_html = models.TextField(
        verbose_name="Conteúdo HTML",
        help_text="Template HTML com variáveis Django"
    )
    
    css_personalizado = models.TextField(
        blank=True,
        null=True,
        verbose_name="CSS Personalizado",
        help_text="Estilos CSS específicos para este template"
    )
    
    variaveis_disponiveis = models.TextField(
        blank=True,
        null=True,
        verbose_name="Variáveis Disponíveis",
        help_text="Lista de variáveis que podem ser usadas no template"
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Template Ativo"
    )
    
    padrao = models.BooleanField(
        default=False,
        verbose_name="Template Padrão",
        help_text="Template padrão para este tipo de documento"
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
        verbose_name = "Template de Documento"
        verbose_name_plural = "Templates de Documentos"
        ordering = ['tipo', 'nome']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nome}"
    
    def save(self, *args, **kwargs):
        """Garante que apenas um template seja padrão por tipo."""
        if self.padrao:
            # Remove padrão de outros templates do mesmo tipo
            TemplateDocumento.objects.filter(
                tipo=self.tipo, 
                padrao=True
            ).exclude(pk=self.pk).update(padrao=False)
        super().save(*args, **kwargs)


class DocumentoGerado(models.Model):
    """Documentos gerados a partir dos templates."""
    
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('gerado', 'Gerado'),
        ('enviado', 'Enviado'),
        ('assinado', 'Assinado'),
        ('arquivado', 'Arquivado'),
    ]
    
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID do Documento"
    )
    
    template = models.ForeignKey(
        TemplateDocumento,
        on_delete=models.PROTECT,
        verbose_name="Template Utilizado"
    )
    
    pessoa_falecida = models.ForeignKey(
        PessoaFalecida,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Pessoa Falecida"
    )
    
    familia = models.ForeignKey(
        Familia,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Família"
    )
    
    servico_contratado = models.ForeignKey(
        ServicoContratado,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Serviço Contratado"
    )
    
    titulo = models.CharField(
        max_length=300,
        verbose_name="Título do Documento"
    )
    
    conteudo_html = models.TextField(
        verbose_name="Conteúdo HTML Gerado"
    )
    
    arquivo_pdf = models.FileField(
        upload_to='documentos/pdfs/',
        blank=True,
        null=True,
        verbose_name="Arquivo PDF"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='rascunho',
        verbose_name="Status"
    )
    
    publico = models.BooleanField(
        default=False,
        verbose_name="Documento Público",
        help_text="Permite acesso via URL pública"
    )
    
    senha_acesso = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Senha de Acesso",
        help_text="Senha para acesso ao documento público"
    )
    
    data_expiracao = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data de Expiração",
        help_text="Data limite para acesso público"
    )
    
    visualizacoes = models.PositiveIntegerField(
        default=0,
        verbose_name="Número de Visualizações"
    )
    
    usuario_criador = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Usuário Criador"
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
        verbose_name = "Documento Gerado"
        verbose_name_plural = "Documentos Gerados"
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"
    
    def get_absolute_url(self):
        """Retorna URL absoluta do documento."""
        return reverse('documentos:visualizar', kwargs={'uuid': self.uuid})
    
    def get_public_url(self):
        """Retorna URL pública do documento."""
        if self.publico:
            return reverse('documentos:publico', kwargs={'uuid': self.uuid})
        return None
    
    def get_pdf_url(self):
        """Retorna URL do PDF se existir."""
        if self.arquivo_pdf:
            return self.arquivo_pdf.url
        return None
    
    def incrementar_visualizacao(self):
        """Incrementa contador de visualizações."""
        self.visualizacoes += 1
        self.save(update_fields=['visualizacoes'])


class CompartilhamentoDocumento(models.Model):
    """Registro de compartilhamentos de documentos."""
    
    PLATAFORMA_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('email', 'Email'),
        ('link_direto', 'Link Direto'),
        ('qr_code', 'QR Code'),
    ]
    
    documento = models.ForeignKey(
        DocumentoGerado,
        on_delete=models.CASCADE,
        verbose_name="Documento"
    )
    
    plataforma = models.CharField(
        max_length=20,
        choices=PLATAFORMA_CHOICES,
        verbose_name="Plataforma"
    )
    
    destinatario = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Destinatário",
        help_text="Email, telefone ou nome do destinatário"
    )
    
    mensagem_personalizada = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mensagem Personalizada"
    )
    
    data_compartilhamento = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data do Compartilhamento"
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Usuário que Compartilhou"
    )
    
    class Meta:
        verbose_name = "Compartilhamento de Documento"
        verbose_name_plural = "Compartilhamentos de Documentos"
        ordering = ['-data_compartilhamento']
    
    def __str__(self):
        return f"{self.documento.titulo} - {self.get_plataforma_display()}"


class MetaTagsDocumento(models.Model):
    """Meta tags para compartilhamento em redes sociais."""
    
    documento = models.OneToOneField(
        DocumentoGerado,
        on_delete=models.CASCADE,
        verbose_name="Documento"
    )
    
    # Open Graph (Facebook, LinkedIn)
    og_title = models.CharField(
        max_length=200,
        verbose_name="OG Title"
    )
    
    og_description = models.TextField(
        max_length=300,
        verbose_name="OG Description"
    )
    
    og_image = models.ImageField(
        upload_to='documentos/og_images/',
        blank=True,
        null=True,
        verbose_name="OG Image"
    )
    
    og_type = models.CharField(
        max_length=50,
        default='article',
        verbose_name="OG Type"
    )
    
    # Twitter Cards
    twitter_card = models.CharField(
        max_length=50,
        default='summary_large_image',
        verbose_name="Twitter Card"
    )
    
    twitter_title = models.CharField(
        max_length=200,
        verbose_name="Twitter Title"
    )
    
    twitter_description = models.TextField(
        max_length=200,
        verbose_name="Twitter Description"
    )
    
    twitter_image = models.ImageField(
        upload_to='documentos/twitter_images/',
        blank=True,
        null=True,
        verbose_name="Twitter Image"
    )
    
    # WhatsApp
    whatsapp_title = models.CharField(
        max_length=200,
        verbose_name="WhatsApp Title"
    )
    
    whatsapp_description = models.TextField(
        max_length=300,
        verbose_name="WhatsApp Description"
    )
    
    class Meta:
        verbose_name = "Meta Tags do Documento"
        verbose_name_plural = "Meta Tags dos Documentos"
    
    def __str__(self):
        return f"Meta Tags - {self.documento.titulo}"
