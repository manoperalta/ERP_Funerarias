from django.db import models
from django.core.validators import RegexValidator


class ConfiguracaoFuneraria(models.Model):
    """Modelo para configurações gerais da funerária."""
    
    # Informações básicas
    nome_funeraria = models.CharField(
        max_length=200,
        default="Sistema Funerária",
        verbose_name="Nome da Funerária",
        help_text="Nome que aparecerá no sistema"
    )
    
    slogan = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Slogan",
        help_text="Frase que representa a funerária"
    )
    
    # Imagens
    logo = models.ImageField(
        upload_to='configuracoes/logos/',
        blank=True,
        null=True,
        verbose_name="Logo",
        help_text="Logo da funerária (recomendado: 200x80px)"
    )
    
    favicon = models.ImageField(
        upload_to='configuracoes/favicons/',
        blank=True,
        null=True,
        verbose_name="Favicon",
        help_text="Ícone do site (recomendado: 32x32px)"
    )
    
    # Informações de contato
    telefone_principal = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone Principal",
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Formato: (11) 99999-9999'
        )]
    )
    
    telefone_secundario = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone Secundário",
        validators=[RegexValidator(
            regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
            message='Formato: (11) 99999-9999'
        )]
    )
    
    email_principal = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email Principal"
    )
    
    email_comercial = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email Comercial"
    )
    
    # Endereço
    endereco_completo = models.TextField(
        blank=True,
        null=True,
        verbose_name="Endereço Completo",
        help_text="Endereço completo da funerária"
    )
    
    cep = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="CEP",
        validators=[RegexValidator(
            regex=r'^\d{5}-\d{3}$',
            message='Formato: 12345-678'
        )]
    )
    
    cidade = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Cidade"
    )
    
    estado = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        verbose_name="Estado (UF)"
    )
    
    # Informações legais
    cnpj = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        verbose_name="CNPJ",
        validators=[RegexValidator(
            regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
            message='Formato: 12.345.678/0001-90'
        )]
    )
    
    inscricao_estadual = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Inscrição Estadual"
    )
    
    # Redes sociais
    facebook_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Facebook URL"
    )
    
    instagram_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Instagram URL"
    )
    
    whatsapp_numero = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="WhatsApp",
        help_text="Número com código do país (5511999999999)"
    )
    
    # Configurações de aparência
    cor_primaria = models.CharField(
        max_length=7,
        default="#0d6efd",
        verbose_name="Cor Primária",
        help_text="Cor principal do sistema (formato: #000000)"
    )
    
    cor_secundaria = models.CharField(
        max_length=7,
        default="#6c757d",
        verbose_name="Cor Secundária",
        help_text="Cor secundária do sistema (formato: #000000)"
    )
    
    # Horário de funcionamento
    horario_funcionamento = models.TextField(
        blank=True,
        null=True,
        verbose_name="Horário de Funcionamento",
        help_text="Horários de atendimento da funerária"
    )
    
    # Configurações do sistema
    ativa = models.BooleanField(
        default=True,
        verbose_name="Configuração Ativa",
        help_text="Apenas uma configuração pode estar ativa por vez"
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
        verbose_name = "Configuração da Funerária"
        verbose_name_plural = "Configurações da Funerária"
        ordering = ['-ativa', '-data_atualizacao']
    
    def __str__(self):
        return f"{self.nome_funeraria} {'(Ativa)' if self.ativa else ''}"
    
    def save(self, *args, **kwargs):
        """Garante que apenas uma configuração esteja ativa por vez."""
        if self.ativa:
            # Desativa todas as outras configurações
            ConfiguracaoFuneraria.objects.filter(ativa=True).update(ativa=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_configuracao_ativa(cls):
        """Retorna a configuração ativa ou cria uma padrão."""
        try:
            return cls.objects.get(ativa=True)
        except cls.DoesNotExist:
            # Cria configuração padrão se não existir
            return cls.objects.create(
                nome_funeraria="Sistema Funerária",
                ativa=True
            )
    
    def get_whatsapp_link(self):
        """Retorna link do WhatsApp formatado."""
        if self.whatsapp_numero:
            return f"https://wa.me/{self.whatsapp_numero}"
        return None
    
    def get_endereco_formatado(self):
        """Retorna endereço formatado para exibição."""
        partes = []
        if self.endereco_completo:
            partes.append(self.endereco_completo)
        if self.cidade and self.estado:
            partes.append(f"{self.cidade}/{self.estado}")
        if self.cep:
            partes.append(f"CEP: {self.cep}")
        return " - ".join(partes) if partes else None
