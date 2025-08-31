from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify
from .models import DocumentoGerado, MetaTagsDocumento, TemplateDocumento
from configuracoes.models import ConfiguracaoFuneraria


@receiver(post_save, sender=DocumentoGerado)
def criar_meta_tags_documento(sender, instance, created, **kwargs):
    """Cria automaticamente meta tags para documentos gerados."""
    if created:
        # Obtém configuração da funerária
        configuracao = ConfiguracaoFuneraria.get_configuracao_ativa()
        
        # Gera título e descrição baseados no documento
        og_title = f"{instance.titulo} - {configuracao.nome_funeraria if configuracao else 'Sistema Funerária'}"
        og_description = f"Documento gerado pelo sistema de gestão funerária"
        
        if instance.pessoa_falecida:
            og_description = f"Memorial de {instance.pessoa_falecida.nome} - {configuracao.nome_funeraria if configuracao else 'Sistema Funerária'}"
        elif instance.familia:
            og_description = f"Documento da família {instance.familia.nome_responsavel} - {configuracao.nome_funeraria if configuracao else 'Sistema Funerária'}"
        
        # Cria meta tags se não existirem
        if not hasattr(instance, 'metatagsdocumento'):
            MetaTagsDocumento.objects.create(
                documento=instance,
                og_title=og_title[:200],  # Limita tamanho
                og_description=og_description[:300],
                twitter_title=og_title[:200],
                twitter_description=og_description[:200],
                whatsapp_title=og_title[:200],
                whatsapp_description=og_description[:300],
            )


@receiver(post_save, sender=DocumentoGerado)
def atualizar_status_documento(sender, instance, created, **kwargs):
    """Atualiza status do documento baseado em condições."""
    if created and instance.status == 'rascunho':
        # Se tem conteúdo HTML, marca como gerado
        if instance.conteudo_html and len(instance.conteudo_html.strip()) > 50:
            instance.status = 'gerado'
            instance.save(update_fields=['status'])


@receiver(post_save, sender=DocumentoGerado)
def log_criacao_documento(sender, instance, created, **kwargs):
    """Registra log da criação de documentos para auditoria."""
    if created:
        # Aqui poderia integrar com sistema de logs mais avançado
        print(f"[LOG] Documento criado: {instance.titulo} por {instance.usuario_criador.username}")


@receiver(pre_delete, sender=DocumentoGerado)
def log_exclusao_documento(sender, instance, **kwargs):
    """Registra log da exclusão de documentos."""
    print(f"[LOG] Documento excluído: {instance.titulo} (UUID: {instance.uuid})")


@receiver(post_save, sender=TemplateDocumento)
def validar_template_padrao(sender, instance, created, **kwargs):
    """Garante que apenas um template seja padrão por tipo."""
    if instance.padrao:
        # Remove padrão de outros templates do mesmo tipo
        TemplateDocumento.objects.filter(
            tipo=instance.tipo,
            padrao=True
        ).exclude(pk=instance.pk).update(padrao=False)

