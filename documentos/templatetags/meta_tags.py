from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
from urllib.parse import urljoin

register = template.Library()


@register.inclusion_tag('documentos/meta_tags/open_graph.html', takes_context=True)
def open_graph_tags(context, documento=None, title=None, description=None, image=None, url=None):
    """Gera meta tags Open Graph para Facebook, LinkedIn, etc."""
    request = context['request']
    meta_tags = context.get('meta_tags', {})
    
    # Valores padrão ou específicos do documento
    if documento and hasattr(documento, 'metatagsdocumento'):
        meta = documento.metatagsdocumento
        og_title = meta.og_title
        og_description = meta.og_description
        og_image = meta.og_image.url if meta.og_image else None
        og_type = meta.og_type
    else:
        og_title = title or meta_tags.get('site_name', 'Sistema Funerária')
        og_description = description or meta_tags.get('site_description', 'Sistema de gestão funerária')
        og_image = image or meta_tags.get('site_logo')
        og_type = 'website'
    
    og_url = url or request.build_absolute_uri()
    
    # Converte URLs relativas em absolutas
    if og_image and not og_image.startswith('http'):
        og_image = request.build_absolute_uri(og_image)
    
    return {
        'og_title': og_title,
        'og_description': og_description,
        'og_image': og_image,
        'og_url': og_url,
        'og_type': og_type,
        'site_name': meta_tags.get('site_name', 'Sistema Funerária'),
    }


@register.inclusion_tag('documentos/meta_tags/twitter_cards.html', takes_context=True)
def twitter_card_tags(context, documento=None, title=None, description=None, image=None):
    """Gera meta tags Twitter Cards."""
    request = context['request']
    meta_tags = context.get('meta_tags', {})
    
    # Valores padrão ou específicos do documento
    if documento and hasattr(documento, 'metatagsdocumento'):
        meta = documento.metatagsdocumento
        twitter_title = meta.twitter_title
        twitter_description = meta.twitter_description
        twitter_image = meta.twitter_image.url if meta.twitter_image else None
        twitter_card = meta.twitter_card
    else:
        twitter_title = title or meta_tags.get('site_name', 'Sistema Funerária')
        twitter_description = description or meta_tags.get('site_description', 'Sistema de gestão funerária')
        twitter_image = image or meta_tags.get('site_logo')
        twitter_card = 'summary_large_image'
    
    # Converte URLs relativas em absolutas
    if twitter_image and not twitter_image.startswith('http'):
        twitter_image = request.build_absolute_uri(twitter_image)
    
    return {
        'twitter_card': twitter_card,
        'twitter_title': twitter_title,
        'twitter_description': twitter_description,
        'twitter_image': twitter_image,
    }


@register.inclusion_tag('documentos/meta_tags/whatsapp.html', takes_context=True)
def whatsapp_meta_tags(context, documento=None, title=None, description=None, image=None):
    """Gera meta tags específicas para WhatsApp."""
    request = context['request']
    meta_tags = context.get('meta_tags', {})
    
    # Valores padrão ou específicos do documento
    if documento and hasattr(documento, 'metatagsdocumento'):
        meta = documento.metatagsdocumento
        whatsapp_title = meta.whatsapp_title
        whatsapp_description = meta.whatsapp_description
    else:
        whatsapp_title = title or meta_tags.get('site_name', 'Sistema Funerária')
        whatsapp_description = description or meta_tags.get('site_description', 'Sistema de gestão funerária')
    
    whatsapp_image = image or meta_tags.get('site_logo')
    
    # Converte URLs relativas em absolutas
    if whatsapp_image and not whatsapp_image.startswith('http'):
        whatsapp_image = request.build_absolute_uri(whatsapp_image)
    
    return {
        'whatsapp_title': whatsapp_title,
        'whatsapp_description': whatsapp_description,
        'whatsapp_image': whatsapp_image,
    }


@register.simple_tag(takes_context=True)
def whatsapp_share_url(context, documento=None, message=None):
    """Gera URL para compartilhamento no WhatsApp."""
    request = context['request']
    meta_tags = context.get('meta_tags', {})
    
    if documento:
        url = request.build_absolute_uri(documento.get_public_url() or documento.get_absolute_url())
        default_message = f"Confira este documento: {documento.titulo}"
    else:
        url = request.build_absolute_uri()
        default_message = f"Confira nosso sistema: {meta_tags.get('site_name', 'Sistema Funerária')}"
    
    message = message or default_message
    whatsapp_url = f"https://wa.me/?text={escape(message)} {url}"
    
    return whatsapp_url


@register.simple_tag(takes_context=True)
def facebook_share_url(context, documento=None):
    """Gera URL para compartilhamento no Facebook."""
    request = context['request']
    
    if documento:
        url = request.build_absolute_uri(documento.get_public_url() or documento.get_absolute_url())
    else:
        url = request.build_absolute_uri()
    
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={url}"
    return facebook_url


@register.simple_tag(takes_context=True)
def twitter_share_url(context, documento=None, text=None):
    """Gera URL para compartilhamento no Twitter."""
    request = context['request']
    meta_tags = context.get('meta_tags', {})
    
    if documento:
        url = request.build_absolute_uri(documento.get_public_url() or documento.get_absolute_url())
        default_text = f"Confira este documento: {documento.titulo}"
    else:
        url = request.build_absolute_uri()
        default_text = f"Confira nosso sistema: {meta_tags.get('site_name', 'Sistema Funerária')}"
    
    text = text or default_text
    twitter_url = f"https://twitter.com/intent/tweet?text={escape(text)}&url={url}"
    
    return twitter_url


@register.simple_tag
def generate_qr_code(url, size=200):
    """Gera URL para QR Code usando serviço online."""
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={url}"
    return qr_url


@register.filter
def truncate_description(text, length=160):
    """Trunca descrição para meta tags respeitando limite de caracteres."""
    if not text:
        return ""
    
    if len(text) <= length:
        return text
    
    # Trunca no último espaço antes do limite
    truncated = text[:length].rsplit(' ', 1)[0]
    return f"{truncated}..."

