from django.shortcuts import render, get_object_or_404
from pessoa_falecida.models import PessoaFalecida
from agendamento.models import Agendamento

def post_lembranca_view(request, pk):
    pessoa_falecida = get_object_or_404(PessoaFalecida, pk=pk)
    agendamento = Agendamento.objects.filter(pessoa_falecida=pessoa_falecida).first()
    
    context = {
        'pessoa_falecida': pessoa_falecida,
        'agendamento': agendamento,
    }
    return render(request, 'documentos/post_lembranca.html', context)


