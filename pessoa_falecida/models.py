from django.db import models
from familia.models import Familia


class PessoaFalecida(models.Model):
    """Modelo para representar pessoas falecidas."""
    
    nome = models.CharField(max_length=200, verbose_name="Nome")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    data_falecimento = models.DateField(verbose_name="Data de Falecimento")
    causa_obito = models.TextField(verbose_name="Causa do Óbito")
    local_obito = models.CharField(max_length=200, verbose_name="Local do Óbito")
    documento_cpf_rg = models.CharField(max_length=20, verbose_name="CPF/RG")
    familia = models.ForeignKey(
        Familia, 
        on_delete=models.CASCADE, 
        verbose_name="Família",
        related_name="pessoas_falecidas"
    )
    imagem = models.ImageField(upload_to='pessoas_falecidas/', blank=True, null=True, verbose_name="Foto do Falecido")
    
    class Meta:
        verbose_name = "Pessoa Falecida"
        verbose_name_plural = "Pessoas Falecidas"
        ordering = ['-data_falecimento']
    
    def __str__(self):
        return f"{self.nome} - {self.data_falecimento}"
    
    @property
    def idade_obito(self):
        """Calcula a idade no momento do óbito."""
        return (self.data_falecimento - self.data_nascimento).days // 365
