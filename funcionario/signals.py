from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Funcionario
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Funcionario)
def criar_conta_funcionario(sender, instance, created, **kwargs):
    """
    Cria automaticamente uma conta de usuário quando um funcionário é criado.
    """
    if created and not instance.usuario:
        try:
            # Gerar username único
            username_base = instance.username_sugerido
            username = username_base
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{username_base}{counter}"
                counter += 1
            
            # Criar usuário
            usuario = User.objects.create_user(
                username=username,
                email=instance.email,
                first_name=instance.nome.split()[0] if instance.nome.split() else '',
                last_name=' '.join(instance.nome.split()[1:]) if len(instance.nome.split()) > 1 else '',
                cargo=instance.cargo,
                telefone=instance.telefone,
                password='123456'  # Senha padrão - deve ser alterada no primeiro login
            )
            
            # Associar usuário ao funcionário
            instance.usuario = usuario
            instance.save(update_fields=['usuario'])
            
            logger.info(f"Conta criada para funcionário {instance.nome}: {username}")
            
        except Exception as e:
            logger.error(f"Erro ao criar conta para funcionário {instance.nome}: {e}")


@receiver(post_delete, sender=Funcionario)
def deletar_conta_funcionario(sender, instance, **kwargs):
    """
    Remove a conta de usuário quando um funcionário é deletado.
    """
    if instance.usuario:
        try:
            usuario = instance.usuario
            usuario.delete()
            logger.info(f"Conta removida para funcionário {instance.nome}")
        except Exception as e:
            logger.error(f"Erro ao remover conta do funcionário {instance.nome}: {e}")


def criar_contas_funcionarios_existentes():
    """
    Função utilitária para criar contas para funcionários existentes que não possuem.
    """
    funcionarios_sem_conta = Funcionario.objects.filter(usuario__isnull=True, ativo=True)
    
    for funcionario in funcionarios_sem_conta:
        try:
            # Gerar username único
            username_base = funcionario.username_sugerido
            username = username_base
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{username_base}{counter}"
                counter += 1
            
            # Criar usuário
            usuario = User.objects.create_user(
                username=username,
                email=funcionario.email,
                first_name=funcionario.nome.split()[0] if funcionario.nome.split() else '',
                last_name=' '.join(funcionario.nome.split()[1:]) if len(funcionario.nome.split()) > 1 else '',
                cargo=funcionario.cargo,
                telefone=funcionario.telefone,
                password='123456'
            )
            
            # Associar usuário ao funcionário
            funcionario.usuario = usuario
            funcionario.save(update_fields=['usuario'])
            
            print(f"✅ Conta criada: {funcionario.nome} -> {username}")
            
        except Exception as e:
            print(f"❌ Erro ao criar conta para {funcionario.nome}: {e}")
    
    print(f"\n🎉 Processo concluído! {funcionarios_sem_conta.count()} contas criadas.")

