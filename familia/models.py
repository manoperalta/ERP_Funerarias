from django.db import models


class Familia(models.Model):
    """Modelo para representar famílias dos falecidos."""
    
    nome_responsavel = models.CharField(max_length=200, verbose_name="Nome do Responsável")
    grau_parentesco = models.CharField(max_length=100, verbose_name="Grau de Parentesco")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    endereco = models.TextField(verbose_name="Endereço")
    
    class Meta:
        verbose_name = "Família"
        verbose_name_plural = "Famílias"
        ordering = ['nome_responsavel']
    
    def __str__(self):
        return f"{self.nome_responsavel} ({self.grau_parentesco})"
