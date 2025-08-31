from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ProdutoEstoque, MovimentacaoEstoque, AlertaEstoque


@receiver(post_save, sender=ProdutoEstoque)
def verificar_alertas_estoque(sender, instance, created, **kwargs):
    """Verifica e cria alertas automáticos para estoque."""
    # Remove alertas antigos do produto
    AlertaEstoque.objects.filter(
        produto=instance,
        ativo=True
    ).update(ativo=False, data_resolucao=timezone.now())
    
    # Verifica estoque baixo
    if instance.estoque_baixo:
        AlertaEstoque.objects.create(
            produto=instance,
            tipo_alerta='estoque_baixo',
            mensagem=f'Estoque baixo para {instance.nome}. Quantidade atual: {instance.quantidade_atual} {instance.get_unidade_medida_display()}. Mínimo: {instance.quantidade_minima}.'
        )
    
    # Verifica produto zerado
    if instance.quantidade_atual <= 0:
        AlertaEstoque.objects.create(
            produto=instance,
            tipo_alerta='produto_zerado',
            mensagem=f'Produto {instance.nome} está zerado no estoque!'
        )
    
    # Verifica estoque alto
    if instance.estoque_alto:
        AlertaEstoque.objects.create(
            produto=instance,
            tipo_alerta='estoque_alto',
            mensagem=f'Estoque alto para {instance.nome}. Quantidade atual: {instance.quantidade_atual} {instance.get_unidade_medida_display()}. Máximo recomendado: {instance.quantidade_maxima}.'
        )


@receiver(post_save, sender=MovimentacaoEstoque)
def log_movimentacao_estoque(sender, instance, created, **kwargs):
    """Registra log das movimentações de estoque."""
    if created:
        print(f"[LOG ESTOQUE] {instance.get_tipo_display()}: {instance.produto.nome} - Qtd: {instance.quantidade} - Usuário: {instance.usuario.username}")


@receiver(pre_save, sender=MovimentacaoEstoque)
def validar_movimentacao_estoque(sender, instance, **kwargs):
    """Valida movimentações de estoque antes de salvar."""
    # Para saídas, verifica se há estoque suficiente
    if instance.tipo in ['saida', 'perda'] and not instance.pk:
        produto = instance.produto
        if produto.quantidade_atual < instance.quantidade:
            raise ValueError(
                f'Estoque insuficiente para {produto.nome}. '
                f'Disponível: {produto.quantidade_atual}, '
                f'Solicitado: {instance.quantidade}'
            )


@receiver(post_save, sender=ProdutoEstoque)
def atualizar_preco_custo_medio(sender, instance, created, **kwargs):
    """Atualiza preço de custo médio baseado nas últimas movimentações."""
    if not created:
        # Calcula preço médio das últimas 5 entradas
        ultimas_entradas = MovimentacaoEstoque.objects.filter(
            produto=instance,
            tipo='entrada'
        ).order_by('-data_movimentacao')[:5]
        
        if ultimas_entradas:
            preco_medio = sum(mov.preco_unitario for mov in ultimas_entradas) / len(ultimas_entradas)
            
            # Atualiza apenas se a diferença for significativa (mais de 5%)
            diferenca_percentual = abs(instance.preco_custo - preco_medio) / instance.preco_custo * 100
            if diferenca_percentual > 5:
                print(f"[LOG] Preço médio calculado para {instance.nome}: R$ {preco_medio:.2f} (anterior: R$ {instance.preco_custo:.2f})")


@receiver(post_save, sender=AlertaEstoque)
def notificar_alerta_estoque(sender, instance, created, **kwargs):
    """Notifica sobre alertas de estoque (aqui poderia integrar com email/SMS)."""
    if created and instance.ativo:
        print(f"[ALERTA ESTOQUE] {instance.get_tipo_alerta_display()}: {instance.mensagem}")
        
        # Aqui poderia integrar com:
        # - Envio de email para administradores
        # - Notificação push
        # - Integração com WhatsApp Business API
        # - Slack/Discord webhook

