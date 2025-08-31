from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Modelo de usuário personalizado com cargos específicos."""
    
    CARGO_CHOICES = [
        ('adm', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('florista', 'Florista'),
        ('coveiro', 'Coveiro'),
        ('preparador', 'Preparador'),
    ]
    
    cargo = models.CharField(
        max_length=20,
        choices=CARGO_CHOICES,
        verbose_name="Cargo",
        help_text="Cargo do usuário no sistema"
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone"
    )
    data_nascimento = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Nascimento"
    )
    endereco = models.TextField(
        blank=True,
        null=True,
        verbose_name="Endereço"
    )
    foto_perfil = models.ImageField(
        upload_to='perfis/',
        blank=True,
        null=True,
        verbose_name="Foto do Perfil"
    )
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['username']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_cargo_display()})"
    
    @property
    def is_admin(self):
        """Verifica se o usuário é administrador."""
        return self.cargo == 'adm'
    
    @property
    def is_vendedor(self):
        """Verifica se o usuário é vendedor."""
        return self.cargo == 'vendedor'
    
    @property
    def is_funcionario_operacional(self):
        """Verifica se o usuário é funcionário operacional (florista, coveiro, preparador)."""
        return self.cargo in ['florista', 'coveiro', 'preparador']
    
    def get_dashboard_permissions(self):
        """Retorna as permissões do dashboard baseadas no cargo."""
        if self.is_admin:
            return {
                'funcionarios': True,
                'familias': True,
                'pessoas_falecidas': True,
                'itens_servico': True,
                'servicos_contratados': True,
                'agendamentos': True,
                'planejamentos': True,
                'financeiro': True,
                'estoque': True,
                'relatorios': True,
            }
        elif self.is_vendedor:
            return {
                'funcionarios': False,
                'familias': True,
                'pessoas_falecidas': True,
                'itens_servico': True,
                'servicos_contratados': True,
                'agendamentos': True,
                'planejamentos': True,
                'financeiro': True,
                'estoque': False,
                'relatorios': False,
            }
        elif self.is_funcionario_operacional:
            return {
                'funcionarios': False,
                'familias': False,
                'pessoas_falecidas': False,
                'itens_servico': False,
                'servicos_contratados': False,
                'agendamentos': True,  # Apenas sua agenda
                'planejamentos': False,
                'financeiro': False,
                'estoque': False,
                'relatorios': False,
            }
        else:
            return {}
