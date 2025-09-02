from django.contrib.auth import get_user_model
from .models import Funcionario
import random
import string

User = get_user_model()


def gerar_senha_temporaria(length=8):
    """Gera uma senha temporária aleatória."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def criar_conta_funcionario(funcionario):
    """
    Cria uma conta de usuário para um funcionário específico.
    
    Args:
        funcionario: Instância do modelo Funcionario
        
    Returns:
        tuple: (usuario_criado, senha_gerada) ou (None, None) se houver erro
    """
    if funcionario.usuario:
        return None, None  # Já possui conta
    
    try:
        # Gerar username único
        username_base = funcionario.username_sugerido
        username = username_base
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{username_base}{counter}"
            counter += 1
        
        # Gerar senha temporária
        senha_temporaria = gerar_senha_temporaria()
        
        # Criar usuário
        usuario = User.objects.create_user(
            username=username,
            email=funcionario.email,
            first_name=funcionario.nome.split()[0] if funcionario.nome.split() else '',
            last_name=' '.join(funcionario.nome.split()[1:]) if len(funcionario.nome.split()) > 1 else '',
            cargo=funcionario.cargo,
            telefone=funcionario.telefone,
            password=senha_temporaria
        )
        
        # Associar usuário ao funcionário
        funcionario.usuario = usuario
        funcionario.save(update_fields=['usuario'])
        
        return usuario, senha_temporaria
        
    except Exception as e:
        print(f"Erro ao criar conta para {funcionario.nome}: {e}")
        return None, None


def resetar_senha_funcionario(funcionario):
    """
    Reseta a senha de um funcionário.
    
    Args:
        funcionario: Instância do modelo Funcionario
        
    Returns:
        str: Nova senha ou None se houver erro
    """
    if not funcionario.usuario:
        return None
    
    try:
        nova_senha = gerar_senha_temporaria()
        funcionario.usuario.set_password(nova_senha)
        funcionario.usuario.save()
        return nova_senha
    except Exception as e:
        print(f"Erro ao resetar senha para {funcionario.nome}: {e}")
        return None


def desativar_conta_funcionario(funcionario):
    """
    Desativa a conta de um funcionário sem deletá-la.
    
    Args:
        funcionario: Instância do modelo Funcionario
    """
    if funcionario.usuario:
        funcionario.usuario.is_active = False
        funcionario.usuario.save()
        funcionario.ativo = False
        funcionario.save(update_fields=['ativo'])


def ativar_conta_funcionario(funcionario):
    """
    Ativa a conta de um funcionário.
    
    Args:
        funcionario: Instância do modelo Funcionario
    """
    if funcionario.usuario:
        funcionario.usuario.is_active = True
        funcionario.usuario.save()
        funcionario.ativo = True
        funcionario.save(update_fields=['ativo'])


def sincronizar_dados_funcionario(funcionario):
    """
    Sincroniza os dados do funcionário com sua conta de usuário.
    
    Args:
        funcionario: Instância do modelo Funcionario
    """
    if not funcionario.usuario:
        return
    
    usuario = funcionario.usuario
    nome_parts = funcionario.nome.split()
    
    # Atualizar dados do usuário
    usuario.email = funcionario.email
    usuario.first_name = nome_parts[0] if nome_parts else ''
    usuario.last_name = ' '.join(nome_parts[1:]) if len(nome_parts) > 1 else ''
    usuario.cargo = funcionario.cargo
    usuario.telefone = funcionario.telefone
    usuario.is_active = funcionario.ativo
    
    usuario.save()


def listar_funcionarios_sem_conta():
    """
    Lista funcionários que não possuem conta de usuário.
    
    Returns:
        QuerySet: Funcionários sem conta
    """
    return Funcionario.objects.filter(usuario__isnull=True, ativo=True)


def estatisticas_contas_funcionarios():
    """
    Retorna estatísticas sobre as contas dos funcionários.
    
    Returns:
        dict: Estatísticas
    """
    total_funcionarios = Funcionario.objects.filter(ativo=True).count()
    com_conta = Funcionario.objects.filter(usuario__isnull=False, ativo=True).count()
    sem_conta = total_funcionarios - com_conta
    
    return {
        'total_funcionarios': total_funcionarios,
        'com_conta': com_conta,
        'sem_conta': sem_conta,
        'percentual_com_conta': (com_conta / total_funcionarios * 100) if total_funcionarios > 0 else 0
    }

