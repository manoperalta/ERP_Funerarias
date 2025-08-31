from django.db import models


class Funcionario(models.Model):
    """Modelo para representar funcionários da funerária."""
    
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="Email")
    
    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.cargo}"
