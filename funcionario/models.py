from django.db import models
from accounts.models import CustomUser


class Funcionario(models.Model):
    """Modelo para representar funcionários da funerária."""
    
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cargo = models.CharField(
        max_length=20,
        choices=CustomUser.CARGO_CHOICES,
        verbose_name="Cargo",
        help_text="Cargo do funcionário na funerária"
    )
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="Email")
    usuario = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Conta de Usuário",
        help_text="Conta de login associada ao funcionário"
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Funcionário ativo no sistema"
    )
    
    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.get_cargo_display()}"
    
    def get_cargo_display_name(self):
        """Retorna o nome do cargo para exibição."""
        return self.get_cargo_display()
    
    @property
    def tem_conta_login(self):
        """Verifica se o funcionário possui conta de login."""
        return self.usuario is not None
    
    @property
    def username_sugerido(self):
        """Gera um username sugerido baseado no nome."""
        nome_parts = self.nome.lower().split()
        if len(nome_parts) >= 2:
            return f"{nome_parts[0]}.{nome_parts[-1]}"
        return nome_parts[0] if nome_parts else "funcionario"
