from django import forms
from .models import Agendamento
from pessoa_falecida.models import PessoaFalecida
from funcionario.models import Funcionario


class AgendamentoForm(forms.ModelForm):
    """Formulário para o modelo Agendamento."""
    
    class Meta:
        model = Agendamento
        fields = ['pessoa_falecida', 'funcionario', 'data_agendamento', 'hora_agendamento', 'local_velorio', 'local_sepultamento', 'data_sepultamento']
        widgets = {
            'pessoa_falecida': forms.Select(attrs={
                'class': 'form-select'
            }),
            'funcionario': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_agendamento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'hora_agendamento': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'local_velorio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o local do velório'
            }),
            'local_sepultamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a localização do sepultamento'
            }),
            'data_sepultamento': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'pessoa_falecida': 'Pessoa Falecida',
            'funcionario': 'Funcionário Responsável',
            'data_agendamento': 'Data e Hora do Agendamento',
            'hora_agendamento': 'Hora do Agendamento',
            'local_velorio': 'Local do Velório',
            'local_sepultamento': 'Local do Sepultamento',
            'data_sepultamento': 'Data do Sepultamento',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza os querysets
        self.fields['pessoa_falecida'].queryset = PessoaFalecida.objects.all()
        self.fields['pessoa_falecida'].empty_label = "Selecione uma pessoa"
        
        self.fields['funcionario'].queryset = Funcionario.objects.all()
        self.fields['funcionario'].empty_label = "Selecione um funcionário"
        
    def clean_data_agendamento(self):
        """Validação personalizada para data do agendamento."""
        from django.utils import timezone
        data = self.cleaned_data.get('data_agendamento')
        if data and data < timezone.now():
            raise forms.ValidationError('A data do agendamento não pode ser no passado.')
        return data

