from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
import datetime
from .models import ServicoContratado
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


class ServicoContratadoCreateView(LoginRequiredMixin, CreateView):
    """View para criar um novo serviço contratado."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_form.html'
    fields = ['pessoa_falecida', 'item_servico', 'descricao_adicional', 'valor_final']
    success_url = reverse_lazy('servico_contratado:list')
    
    def form_valid(self, form):
        """Gera número da nota fiscal após salvar."""
        response = super().form_valid(form)
        self.object.gerar_numero_nota_fiscal()
        return response


class ServicoContratadoUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar um serviço contratado."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_form.html'
    fields = ['pessoa_falecida', 'item_servico', 'descricao_adicional', 'valor_final']
    success_url = reverse_lazy('servico_contratado:list')


class ServicoContratadoDeleteView(AdminDeleteMixin, DeleteView):
    """View para excluir um serviço contratado. Restrito a administradores."""
    model = ServicoContratado
    template_name = 'servico_contratado/servico_contratado_confirm_delete.html'
    success_url = reverse_lazy('servico_contratado:list')


@login_required
def gerar_nota_fiscal_pdf(request, pk):
    """Gera nota fiscal em PDF para um serviço contratado."""
    servico = get_object_or_404(ServicoContratado, pk=pk)
    
    # Gera número da nota fiscal se não existir
    if not servico.numero_nota_fiscal:
        servico.gerar_numero_nota_fiscal()
    
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
    
    # Cabeçalho da empresa
    story.append(Paragraph("SISTEMA FUNERÁRIA LTDA", title_style))
    story.append(Paragraph("CNPJ: 12.345.678/0001-90", normal_style))
    story.append(Paragraph("Endereço: Rua das Flores, 123 - Centro - São Paulo/SP", normal_style))
    story.append(Paragraph("Telefone: (11) 3456-7890", normal_style))
    story.append(Spacer(1, 20))
    
    # Título da nota fiscal
    story.append(Paragraph(f"NOTA FISCAL DE SERVIÇO Nº {servico.numero_nota_fiscal}", header_style))
    story.append(Spacer(1, 12))
    
    # Dados do cliente (família)
    if servico.pessoa_falecida.familia:
        familia = servico.pessoa_falecida.familia
        story.append(Paragraph("DADOS DO CLIENTE:", header_style))
        story.append(Paragraph(f"Nome: {familia.nome_responsavel}", normal_style))
        story.append(Paragraph(f"Telefone: {familia.telefone}", normal_style))
        story.append(Paragraph(f"Email: {familia.email}", normal_style))
        story.append(Spacer(1, 12))
    
    # Dados do falecido
    story.append(Paragraph("DADOS DO FALECIDO:", header_style))
    story.append(Paragraph(f"Nome: {servico.pessoa_falecida.nome}", normal_style))
    story.append(Paragraph(f"Data de Nascimento: {servico.pessoa_falecida.data_nascimento.strftime('%d/%m/%Y') if servico.pessoa_falecida.data_nascimento else 'Não informado'}", normal_style))
    story.append(Paragraph(f"Data do Óbito: {servico.pessoa_falecida.data_obito.strftime('%d/%m/%Y') if servico.pessoa_falecida.data_obito else 'Não informado'}", normal_style))
    story.append(Spacer(1, 12))
    
    # Tabela de serviços
    story.append(Paragraph("SERVIÇOS CONTRATADOS:", header_style))
    
    data = [
        ['Descrição', 'Quantidade', 'Valor Unitário', 'Valor Total'],
        [servico.item_servico.nome, '1', f'R$ {servico.item_servico.preco:.2f}', f'R$ {servico.valor_final:.2f}']
    ]
    
    if servico.descricao_adicional:
        data.append(['Observações:', servico.descricao_adicional, '', ''])
    
    table = Table(data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Total
    story.append(Paragraph(f"<b>VALOR TOTAL: R$ {servico.valor_final:.2f}</b>", 
                          ParagraphStyle('Total', parent=normal_style, fontSize=14, alignment=TA_RIGHT)))
    story.append(Spacer(1, 20))
    
    # Informações adicionais
    story.append(Paragraph(f"Data de Emissão: {servico.data_contratacao.strftime('%d/%m/%Y %H:%M')}", normal_style))
    story.append(Paragraph(f"Responsável: {request.user.get_full_name() or request.user.username}", normal_style))
    
    # Rodapé
    story.append(Spacer(1, 30))
    story.append(Paragraph("Esta nota fiscal foi gerada eletronicamente pelo Sistema Funerária.", 
                          ParagraphStyle('Footer', parent=normal_style, fontSize=8, alignment=TA_CENTER)))
    
    # Construir PDF
    doc.build(story)
    
    # Retornar resposta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="nota_fiscal_{servico.numero_nota_fiscal}.pdf"'
    
    return response
