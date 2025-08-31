from configuracoes.models import ConfiguracaoFuneraria


def configuracao_funeraria(request):
    """Context processor para disponibilizar configurações da funerária em todos os templates."""
    try:
        configuracao = ConfiguracaoFuneraria.get_configuracao_ativa()
        return {
            'configuracao_funeraria': configuracao
        }
    except Exception:
        return {
            'configuracao_funeraria': None
        }


def meta_tags_globais(request):
    """Context processor para meta tags globais do sistema."""
    configuracao = ConfiguracaoFuneraria.get_configuracao_ativa()
    
    # Meta tags padrão do sistema
    meta_tags = {
        'site_name': configuracao.nome_funeraria if configuracao else 'Sistema Funerária',
        'site_description': f'Sistema de gestão funerária - {configuracao.slogan}' if configuracao and configuracao.slogan else 'Sistema completo de gestão funerária',
        'site_url': request.build_absolute_uri('/'),
        'site_logo': configuracao.logo.url if configuracao and configuracao.logo else None,
        'site_favicon': configuracao.favicon.url if configuracao and configuracao.favicon else None,
        'site_color': configuracao.cor_primaria if configuracao else '#0d6efd',
        'whatsapp_number': configuracao.whatsapp_numero if configuracao else None,
        'facebook_url': configuracao.facebook_url if configuracao else None,
        'instagram_url': configuracao.instagram_url if configuracao else None,
    }
    
    return {
        'meta_tags': meta_tags
    }

