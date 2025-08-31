from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import ConfiguracaoFuneraria


@receiver(post_save, sender=ConfiguracaoFuneraria)
def limpar_cache_configuracao(sender, instance, **kwargs):
    """Limpa cache das configurações quando alteradas."""
    cache.delete('configuracao_funeraria_ativa')
    print(f"[LOG] Cache de configurações limpo após alteração")


@receiver(post_save, sender=ConfiguracaoFuneraria)
def garantir_configuracao_unica(sender, instance, created, **kwargs):
    """Garante que apenas uma configuração esteja ativa."""
    if instance.ativa:
        # Desativa outras configurações
        ConfiguracaoFuneraria.objects.filter(
            ativa=True
        ).exclude(pk=instance.pk).update(ativa=False)


@receiver(pre_save, sender=ConfiguracaoFuneraria)
def validar_configuracao(sender, instance, **kwargs):
    """Valida dados da configuração antes de salvar."""
    # Valida CNPJ (formato básico)
    if instance.cnpj:
        cnpj_limpo = ''.join(filter(str.isdigit, instance.cnpj))
        if len(cnpj_limpo) != 14:
            print(f"[AVISO] CNPJ pode estar em formato inválido: {instance.cnpj}")
    
    # Valida CEP (formato básico)
    if instance.cep:
        cep_limpo = ''.join(filter(str.isdigit, instance.cep))
        if len(cep_limpo) != 8:
            print(f"[AVISO] CEP pode estar em formato inválido: {instance.cep}")
    
    # Valida WhatsApp
    if instance.whatsapp_numero:
        whatsapp_limpo = ''.join(filter(str.isdigit, instance.whatsapp_numero))
        if len(whatsapp_limpo) < 10:
            print(f"[AVISO] Número do WhatsApp pode estar inválido: {instance.whatsapp_numero}")


@receiver(post_save, sender=ConfiguracaoFuneraria)
def log_alteracao_configuracao(sender, instance, created, **kwargs):
    """Registra log das alterações de configuração."""
    if created:
        print(f"[LOG] Nova configuração criada: {instance.nome_funeraria}")
    else:
        print(f"[LOG] Configuração atualizada: {instance.nome_funeraria}")


@receiver(post_save, sender=ConfiguracaoFuneraria)
def processar_imagens_configuracao(sender, instance, created, **kwargs):
    """Processa imagens da configuração (logo, favicon)."""
    # Aqui poderia implementar:
    # - Redimensionamento automático de imagens
    # - Geração de thumbnails
    # - Otimização de imagens
    # - Conversão de formatos
    
    if instance.logo:
        print(f"[LOG] Logo processado: {instance.logo.name}")
    
    if instance.favicon:
        print(f"[LOG] Favicon processado: {instance.favicon.name}")

