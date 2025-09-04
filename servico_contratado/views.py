from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import datetime
import os
from .models import ServicoContratado, ItemServicoContratado
from .forms import ServicoContratadoForm, ItemServicoContratadoFormSet
from item_servico.models import ItemServico
from app.mixins import LoginRequiredMixin, AdminDeleteMixin


class ServicoContratadoListView(LoginRequiredMixin, ListView):
    """View para listar serviços contratados."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_list.html'
    context_object_name = 'servicos_contratados'
    paginate_by = 10


class ServicoContratadoDetailView(LoginRequiredMixin, DetailView):
    """View para exibir detalhes de um serviço contratado."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_detail.html'
    context_object_name = 'servico_contratado'


def gerar_pdf_nota_fiscal(servico_contratado, usuario):
    """Gera PDF da nota fiscal e salva no modelo."""
    # Gera número da nota fiscal se não existir
    if not servico_contratado.numero_nota_fiscal:
        servico_contratado.gerar_numero_nota_fiscal()
    
    # Criar o PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Conteúdo do PDF
    story = []
    
    # Cabeçalho da empresa (usando dados do usuário/empresa)
    story.append(Paragraph("SISTEMA FUNERÁRIA LTDA", title_style))
    story.append(Paragraph("CNPJ: 12.345.678/0001-90", normal_style))
    story.append(Paragraph("Endereço: Rua das Flores, 123 - Centro - São Paulo/SP", normal_style))
    story.append(Paragraph("Telefone: (11) 3456-7890", normal_style))
    story.append(Paragraph("Email: contato@sistemafuneraria.com.br", normal_style))
    story.append(Spacer(1, 20))
    
    # Título da nota fiscal
    story.append(Paragraph(f"NOTA FISCAL DE SERVIÇO Nº {servico_contratado.numero_nota_fiscal}", header_style))
    story.append(Spacer(1, 12))
    
    # Dados do cliente (família)
    if servico_contratado.pessoa_falecida.familia:
        familia = servico_contratado.pessoa_falecida.familia
        story.append(Paragraph("DADOS DO CLIENTE:", header_style))
        story.append(Paragraph(f"Nome: {familia.nome_responsavel}", normal_style))
        story.append(Paragraph(f"Telefone: {familia.telefone}", normal_style))
        story.append(Paragraph(f"Email: {familia.email}", normal_style))
        story.append(Spacer(1, 12))
    
    # Dados do falecido
    story.append(Paragraph("DADOS DO FALECIDO:", header_style))
    story.append(Paragraph(f"Nome: {servico_contratado.pessoa_falecida.nome}", normal_style))
    story.append(Paragraph(f"Data de Nascimento: {servico_contratado.pessoa_falecida.data_nascimento.strftime('%d/%m/%Y') if servico_contratado.pessoa_falecida.data_nascimento else 'Não informado'}", normal_style))
    story.append(Paragraph(f"Data do Óbito: {servico_contratado.pessoa_falecida.data_falecimento.strftime('%d/%m/%Y') if servico_contratado.pessoa_falecida.data_falecimento else 'Não informado'}", normal_style))
    story.append(Spacer(1, 12))
    
    # Tabela de serviços
    story.append(Paragraph("SERVIÇOS CONTRATADOS:", header_style))
    
    data = [['Descrição', 'Quantidade', 'Valor Unitário', 'Valor Total']]
    
    # Adicionar itens do serviço
    for item in servico_contratado.itens.all():
        data.append([
            item.item_servico.nome,
            str(item.quantidade),
            f'R$ {item.valor_unitario:.2f}',
            f'R$ {item.valor_total:.2f}'
        ])
    
    # Adicionar subtotal, imposto e total
    data.append(['', '', 'Subtotal:', f'R$ {servico_contratado.subtotal:.2f}'])
    data.append(['', '', f'Imposto ({servico_contratado.taxa_imposto}%):', f'R$ {servico_contratado.valor_imposto:.2f}'])
    data.append(['', '', 'TOTAL:', f'R$ {servico_contratado.valor_total:.2f}'])
    
    if servico_contratado.descricao_adicional:
        data.append(['Observações:', servico_contratado.descricao_adicional, '', ''])
    
    table = Table(data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # Destacar totais
        ('FONTNAME', (-2, -3), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Informações adicionais
    story.append(Paragraph(f"Data de Emissão: {servico_contratado.data_contratacao.strftime('%d/%m/%Y %H:%M')}", normal_style))
    story.append(Paragraph(f"Responsável: {usuario.get_full_name() or usuario.username}", normal_style))
    
    # Rodapé
    story.append(Spacer(1, 30))
    story.append(Paragraph("Esta nota fiscal foi gerada eletronicamente pelo Sistema Funerária.", 
                          ParagraphStyle('Footer', parent=normal_style, fontSize=8, alignment=TA_CENTER)))
    
    # Construir PDF
    doc.build(story)
    
    # Salvar PDF no modelo
    buffer.seek(0)
    pdf_content = buffer.getvalue()
    filename = f"nota_fiscal_{servico_contratado.numero_nota_fiscal}.pdf"
    
    servico_contratado.pdf_nota_fiscal.save(
        filename,
        ContentFile(pdf_content),
        save=True
    )
    
    return servico_contratado


@login_required
def servico_contratado_create(request):
    """View para criar um novo serviço contratado com múltiplos itens."""
    if request.method == 'POST':
        form = ServicoContratadoForm(request.POST)
        formset = ItemServicoContratadoFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                servico = form.save()
                formset.instance = servico
                formset.save()
                
                # Gerar PDF automaticamente
                gerar_pdf_nota_fiscal(servico, request.user)
                
                # Criar registro financeiro automaticamente
                from financeiro.models import Financeiro
                from datetime import date, timedelta
                
                Financeiro.objects.create(
                    pessoa_falecida=servico.pessoa_falecida,
                    servico_contratado=servico,
                    tipo='receita',
                    descricao=f'Serviços funerários - {servico.pessoa_falecida.nome}',
                    valor=servico.valor_total,
                    data_vencimento=date.today() + timedelta(days=30),  # 30 dias para pagamento
                    status='pendente'
                )
                
                return redirect('servico_contratado:detail', pk=servico.pk)
    else:
        form = ServicoContratadoForm()
        formset = ItemServicoContratadoFormSet()
    
    return render(request, 'servico_contratado/servico_contratado_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Novo Serviço Contratado'
    })


@login_required
def servico_contratado_update(request, pk):
    """View para atualizar um serviço contratado."""
    servico = get_object_or_404(ServicoContratado, pk=pk)
    
    if request.method == 'POST':
        form = ServicoContratadoForm(request.POST, instance=servico)
        formset = ItemServicoContratadoFormSet(request.POST, instance=servico)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
                
                # Regenerar PDF se houve alterações
                gerar_pdf_nota_fiscal(servico, request.user)
                
                return redirect('servico_contratado:detail', pk=servico.pk)
    else:
        form = ServicoContratadoForm(instance=servico)
        formset = ItemServicoContratadoFormSet(instance=servico)
    
    return render(request, 'servico_contratado/servico_contratado_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Editar Serviço Contratado',
        'object': servico
    })


class ServicoContratadoDeleteView(AdminDeleteMixin, DeleteView):
    """View para excluir um serviço contratado. Restrito a administradores."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_confirm_delete.html'
    success_url = reverse_lazy('servico_contratado:list')


@login_required
def get_item_preco(request, item_id):
    """API para obter o preço de um item de serviço."""
    try:
        item = ItemServico.objects.get(id=item_id)
        return JsonResponse({
            'preco': float(item.preco_unitario),
            'nome': item.nome
        })
    except ItemServico.DoesNotExist:
        return JsonResponse({'error': 'Item não encontrado'}, status=404)


@login_required
def visualizar_nota_fiscal_pdf(request, pk):
    """View para visualizar o PDF da nota fiscal."""
    servico = get_object_or_404(ServicoContratado, pk=pk)
    
    if not servico.pdf_nota_fiscal:
        # Se não existe PDF, gerar um novo
        gerar_pdf_nota_fiscal(servico, request.user)
    
    if servico.pdf_nota_fiscal:
        response = HttpResponse(servico.pdf_nota_fiscal.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="nota_fiscal_{servico.numero_nota_fiscal}.pdf"'
        return response
    else:
        return HttpResponse("Erro ao gerar PDF", status=500)


@login_required
def gerar_nota_fiscal_pdf(request, pk):
    """Gera nota fiscal em PDF para um serviço contratado (mantido para compatibilidade)."""
    servico = get_object_or_404(ServicoContratado, pk=pk)
    
    # Usar a nova função de geração
    gerar_pdf_nota_fiscal(servico, request.user)
    
    # Retornar o PDF
    if servico.pdf_nota_fiscal:
        response = HttpResponse(servico.pdf_nota_fiscal.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="nota_fiscal_{servico.numero_nota_fiscal}.pdf"'
        return response
    else:
        return HttpResponse("Erro ao gerar PDF", status=500)

