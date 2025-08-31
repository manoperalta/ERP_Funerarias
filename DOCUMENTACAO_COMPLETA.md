# Sistema de Gestão Funerária - Documentação Completa

## 📋 Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Funcionalidades Implementadas](#funcionalidades-implementadas)
4. [Instalação e Configuração](#instalação-e-configuração)
5. [Guia de Uso](#guia-de-uso)
6. [Estrutura do Projeto](#estrutura-do-projeto)
7. [Tecnologias Utilizadas](#tecnologias-utilizadas)
8. [Segurança e Auditoria](#segurança-e-auditoria)
9. [Manutenção e Suporte](#manutenção-e-suporte)

---

## 🎯 Visão Geral

O **Sistema de Gestão Funerária** é uma aplicação web completa desenvolvida em Django para gerenciar todos os aspectos operacionais de uma funerária. O sistema oferece controle total sobre funcionários, famílias, pessoas falecidas, serviços, agendamentos, estoque e aspectos financeiros.

### Características Principais
- **Interface Moderna**: Design responsivo com Bootstrap 5
- **Modular**: 12 módulos independentes e integrados
- **Seguro**: Sistema de autenticação com diferentes níveis de acesso
- **Auditoria Completa**: Logs automáticos de todas as operações
- **Compartilhamento Social**: Meta tags otimizadas para redes sociais
- **Gestão de Documentos**: Geração automática de PDF e HTML
- **Controle de Estoque**: Sistema completo com alertas automáticos

---

## 🏗️ Arquitetura do Sistema

### Framework e Versão
- **Django 5.2.5** - Framework web Python
- **Python 3.11** - Linguagem de programação
- **SQLite** - Banco de dados (desenvolvimento)
- **Bootstrap 5.3.0** - Framework CSS

### Padrões Arquiteturais
- **MVT (Model-View-Template)** - Padrão Django
- **Class-Based Views (CBV)** - Views orientadas a objetos
- **PEP 8** - Padrões de codificação Python
- **Modular Design** - Apps independentes e reutilizáveis

### Estrutura de Apps
```
sistema_funeraria/
├── app/                    # Configurações principais
├── accounts/               # Sistema de usuários
├── funcionario/           # Gestão de funcionários
├── familia/               # Cadastro de famílias
├── pessoa_falecida/       # Registro de falecidos
├── item_servico/          # Catálogo de serviços
├── servico_contratado/    # Controle de contratos
├── agendamento/           # Gestão de agenda
├── planejamento/          # Planejamento de serviços
├── financeiro/            # Controle financeiro
├── estoque/               # Sistema de estoque
├── documentos/            # Geração de documentos
├── configuracoes/         # Configurações da funerária
└── templates/             # Templates HTML
```

---


## ⚙️ Funcionalidades Implementadas

### 1. Sistema de Autenticação e Usuários
- **Tipos de Usuário**: Administrador, Vendedor, Florista, Coveiro, Preparador
- **Login/Logout**: Sistema seguro com sessões
- **Dashboards Personalizados**: Interface específica por cargo
- **Controle de Permissões**: Acesso baseado no tipo de usuário
- **Auditoria de Acesso**: Logs de login/logout com IP e timestamp

### 2. Gestão de Funcionários
- **CRUD Completo**: Criar, visualizar, editar, excluir
- **Informações**: Nome, cargo, telefone, email, data de admissão
- **Validações**: Formatos de telefone e email
- **Interface Responsiva**: Tabelas adaptáveis para mobile

### 3. Cadastro de Famílias
- **Dados Completos**: Nome responsável, telefone, email, endereço
- **Relacionamentos**: Vinculação com pessoas falecidas
- **Histórico**: Registro de todos os serviços contratados
- **Comunicação**: Canais de contato organizados

### 4. Registro de Pessoas Falecidas
- **Informações Pessoais**: Nome, data nascimento/óbito, documentos
- **Dados Médicos**: Causa do óbito, médico responsável
- **Família**: Vinculação com responsáveis
- **Serviços**: Histórico de serviços prestados

### 5. Catálogo de Itens e Serviços
- **Produtos**: Caixões, flores, velas, ornamentos
- **Serviços**: Preparação, transporte, cerimônias
- **Preços**: Controle de valores e margens
- **Categorização**: Organização por tipos

### 6. Controle de Serviços Contratados
- **Contratos**: Registro de serviços vendidos
- **Status**: Acompanhamento do andamento
- **Valores**: Controle financeiro detalhado
- **Relacionamentos**: Vinculação com família e falecido

### 7. Sistema de Agendamentos
- **Agenda**: Controle de datas e horários
- **Tipos**: Velório, sepultamento, cremação, reuniões
- **Responsáveis**: Designação de funcionários
- **Notificações**: Alertas automáticos

### 8. Planejamento de Serviços
- **Cronograma**: Sequência de atividades
- **Recursos**: Alocação de funcionários e materiais
- **Checklist**: Verificação de tarefas
- **Coordenação**: Integração entre departamentos

### 9. Controle Financeiro
- **Receitas**: Registro de pagamentos recebidos
- **Despesas**: Controle de gastos operacionais
- **Relatórios**: Análises financeiras
- **Fluxo de Caixa**: Controle de entrada e saída

### 10. Sistema de Estoque
- **Produtos**: Controle de quantidade e localização
- **Movimentações**: Entrada, saída, ajustes, perdas
- **Alertas Automáticos**: Estoque baixo, alto, zerado
- **Fornecedores**: Controle de fornecedores
- **Relatórios**: Análises de estoque e custos

### 11. Geração de Documentos
- **Templates**: Modelos personalizáveis
- **Tipos**: Contratos, certidões, memoriais, orçamentos
- **Formatos**: PDF e HTML
- **Compartilhamento**: URLs públicas e privadas
- **Meta Tags**: Otimização para redes sociais

### 12. Configurações da Funerária
- **Informações Básicas**: Nome, slogan, contatos
- **Identidade Visual**: Logo, favicon, cores
- **Endereço**: Localização completa
- **Redes Sociais**: Links para Facebook, Instagram, WhatsApp
- **Horário**: Funcionamento da empresa

---

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Git (opcional, para clonagem)

### Passo a Passo

#### 1. Clonagem do Projeto
```bash
# Se usando Git
git clone <url-do-repositorio>
cd sistema_funeraria

# Ou extrair o arquivo ZIP fornecido
unzip sistema_funeraria_django.zip
cd sistema_funeraria
```

#### 2. Ambiente Virtual (Recomendado)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

#### 3. Instalação de Dependências
```bash
pip install -r requirements.txt
```

#### 4. Configuração do Banco de Dados
```bash
# Aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser
```

#### 5. Executar o Servidor
```bash
python manage.py runserver
```

#### 6. Acessar o Sistema
- Abra o navegador em: `http://localhost:8000`
- Faça login com as credenciais criadas

### Configurações Adicionais

#### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
```

#### Configuração de Produção
Para ambiente de produção, ajuste:
- `DEBUG = False` no settings.py
- Configure banco de dados PostgreSQL/MySQL
- Configure servidor web (Nginx + Gunicorn)
- Configure HTTPS e certificados SSL

---


## 📖 Guia de Uso

### Primeiro Acesso
1. **Configuração Inicial**: Acesse "Configurações" e preencha os dados da funerária
2. **Cadastro de Funcionários**: Registre os funcionários da empresa
3. **Catálogo de Serviços**: Configure os itens e serviços oferecidos
4. **Estoque Inicial**: Registre os produtos em estoque

### Fluxo Operacional Típico

#### Para Administradores
1. **Gestão Geral**: Acesso completo a todos os módulos
2. **Relatórios**: Análise de performance e financeiro
3. **Configurações**: Personalização do sistema
4. **Controle de Estoque**: Monitoramento e reposição

#### Para Vendedores
1. **Atendimento**: Cadastro de famílias e falecidos
2. **Orçamentos**: Criação de propostas de serviços
3. **Contratos**: Formalização de serviços
4. **Agendamentos**: Organização de cerimônias

#### Para Funcionários Operacionais
1. **Agenda Pessoal**: Visualização de tarefas
2. **Execução**: Registro de atividades realizadas
3. **Comunicação**: Atualizações de status

### Funcionalidades Avançadas

#### Geração de Documentos
1. Acesse o módulo "Documentos"
2. Escolha o tipo de documento
3. Preencha as informações necessárias
4. Gere PDF ou HTML
5. Compartilhe via redes sociais ou email

#### Controle de Estoque
1. Cadastre produtos e categorias
2. Registre movimentações (entrada/saída)
3. Configure alertas de estoque mínimo
4. Monitore relatórios de consumo

#### Sistema de Alertas
- **Estoque Baixo**: Notificação automática
- **Agendamentos**: Lembretes de compromissos
- **Vencimentos**: Alertas de prazos

---

## 📁 Estrutura Detalhada do Projeto

### Diretórios Principais
```
sistema_funeraria/
├── app/                           # Configurações Django
│   ├── __init__.py
│   ├── settings.py               # Configurações principais
│   ├── urls.py                   # URLs principais
│   ├── wsgi.py                   # Configuração WSGI
│   └── context_processors.py     # Processadores de contexto
│
├── accounts/                      # Sistema de usuários
│   ├── models.py                 # Modelo CustomUser
│   ├── views.py                  # Views de autenticação
│   ├── forms.py                  # Formulários de usuário
│   ├── urls.py                   # URLs do app
│   └── signals.py                # Signals de auditoria
│
├── funcionario/                   # Gestão de funcionários
│   ├── models.py                 # Modelo Funcionario
│   ├── views.py                  # CRUD funcionários
│   ├── forms.py                  # Formulários
│   └── urls.py                   # URLs do módulo
│
├── familia/                       # Cadastro de famílias
├── pessoa_falecida/              # Registro de falecidos
├── item_servico/                 # Catálogo de serviços
├── servico_contratado/           # Controle de contratos
├── agendamento/                  # Sistema de agenda
├── planejamento/                 # Planejamento
├── financeiro/                   # Controle financeiro
├── estoque/                      # Sistema de estoque
├── documentos/                   # Geração de documentos
├── configuracoes/                # Configurações
│
├── templates/                     # Templates HTML
│   ├── base.html                 # Template base
│   ├── accounts/                 # Templates de usuário
│   ├── funcionario/              # Templates funcionários
│   ├── familia/                  # Templates famílias
│   └── ...                       # Outros templates
│
├── static/                        # Arquivos estáticos
├── media/                         # Uploads de arquivos
├── requirements.txt               # Dependências Python
├── manage.py                      # Script de gerenciamento
└── db.sqlite3                     # Banco de dados
```

### Modelos de Dados Principais

#### CustomUser
```python
- username: CharField
- email: EmailField
- cargo: CharField (choices)
- telefone: CharField
- data_admissao: DateField
- ativo: BooleanField
```

#### Funcionario
```python
- nome: CharField
- cargo: CharField
- telefone: CharField
- email: EmailField
- data_admissao: DateField
- ativo: BooleanField
```

#### Familia
```python
- nome_responsavel: CharField
- telefone: CharField
- email: EmailField
- endereco: TextField
- cidade: CharField
- cep: CharField
```

#### PessoaFalecida
```python
- nome: CharField
- data_nascimento: DateField
- data_obito: DateField
- cpf: CharField
- rg: CharField
- familia: ForeignKey(Familia)
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 5.2.5**: Framework web Python
- **Python 3.11**: Linguagem de programação
- **SQLite**: Banco de dados (desenvolvimento)
- **Django ORM**: Mapeamento objeto-relacional

### Frontend
- **Bootstrap 5.3.0**: Framework CSS
- **Bootstrap Icons**: Ícones
- **HTML5**: Estrutura das páginas
- **CSS3**: Estilização
- **JavaScript**: Interatividade

### Funcionalidades Especiais
- **Django Signals**: Automação de processos
- **Context Processors**: Dados globais
- **Template Tags**: Funcionalidades customizadas
- **Class-Based Views**: Views orientadas a objetos
- **Django Forms**: Validação de formulários

### Ferramentas de Desenvolvimento
- **PEP 8**: Padrões de codificação
- **Django Admin**: Interface administrativa
- **Django Debug Toolbar**: Debug (desenvolvimento)
- **Git**: Controle de versão

---

## 🔒 Segurança e Auditoria

### Medidas de Segurança Implementadas

#### Autenticação e Autorização
- **Sistema de Login**: Autenticação obrigatória
- **Controle de Sessões**: Gerenciamento seguro
- **Níveis de Acesso**: Permissões por cargo
- **Logout Automático**: Timeout de sessão

#### Proteção de Dados
- **CSRF Protection**: Proteção contra ataques CSRF
- **XSS Protection**: Sanitização de dados
- **SQL Injection**: Proteção via Django ORM
- **Validação de Entrada**: Validação rigorosa de formulários

#### Auditoria Completa
- **Logs de Acesso**: Registro de login/logout
- **Logs de Operações**: Todas as ações são registradas
- **Rastreamento de IP**: Identificação de origem
- **Timestamp**: Data e hora de todas as operações

### Sistema de Logs
```python
# Exemplos de logs automáticos:
[LOG USER] Novo usuário criado: admin - Cargo: adm
[LOG LOGIN] admin (adm) - IP: 192.168.1.100 - 2025-08-31 06:55:19
[LOG ESTOQUE] Entrada: Caixão Premium - Qtd: 5 - Usuário: admin
[ALERTA ESTOQUE] Estoque baixo: Flores Naturais - Qtd atual: 2
```

### Backup e Recuperação
- **Backup Automático**: Configurável via cron
- **Exportação de Dados**: Funcionalidade de export
- **Recuperação**: Procedimentos documentados
- **Versionamento**: Controle de versões do código

---

## 🔧 Manutenção e Suporte

### Manutenção Preventiva

#### Banco de Dados
```bash
# Limpeza de sessões expiradas
python manage.py clearsessions

# Verificação de integridade
python manage.py check

# Backup do banco
python manage.py dumpdata > backup.json
```

#### Logs e Monitoramento
- **Rotação de Logs**: Configurar logrotate
- **Monitoramento**: Verificar uso de recursos
- **Performance**: Análise de queries lentas
- **Espaço em Disco**: Monitorar crescimento do banco

### Atualizações e Melhorias

#### Processo de Atualização
1. **Backup Completo**: Antes de qualquer alteração
2. **Ambiente de Teste**: Testar em ambiente separado
3. **Migrações**: Aplicar migrações do banco
4. **Testes**: Verificar funcionalidades
5. **Deploy**: Aplicar em produção

#### Melhorias Futuras Sugeridas
- **API REST**: Para integração com outros sistemas
- **Relatórios Avançados**: Dashboard com gráficos
- **Notificações Push**: Alertas em tempo real
- **App Mobile**: Aplicativo para dispositivos móveis
- **Integração WhatsApp**: API para comunicação
- **Backup na Nuvem**: Armazenamento seguro

### Suporte Técnico

#### Problemas Comuns e Soluções

**Erro 500 - Internal Server Error**
```bash
# Verificar logs
python manage.py check
# Verificar migrações
python manage.py showmigrations
```

**Problemas de Permissão**
```bash
# Verificar usuários
python manage.py shell
>>> from accounts.models import CustomUser
>>> CustomUser.objects.all()
```

**Banco de Dados Corrompido**
```bash
# Restaurar backup
python manage.py loaddata backup.json
```

#### Contato para Suporte
- **Documentação**: Este arquivo
- **Logs do Sistema**: Verificar console do Django
- **Comunidade Django**: https://docs.djangoproject.com/

---

## 📊 Estatísticas do Projeto

### Métricas de Desenvolvimento
- **Linhas de Código**: ~5.000 linhas
- **Arquivos Python**: 50+ arquivos
- **Templates HTML**: 30+ templates
- **Modelos de Dados**: 15+ modelos
- **Views**: 40+ views
- **URLs**: 50+ rotas

### Funcionalidades Implementadas
- **Apps Django**: 12 aplicações
- **CRUDs Completos**: 8 módulos
- **Sistema de Usuários**: 5 tipos de cargo
- **Signals Automáticos**: 15+ signals
- **Template Tags**: 10+ tags customizadas
- **Context Processors**: 2 processadores

### Tempo de Desenvolvimento
- **Planejamento**: 2 horas
- **Desenvolvimento**: 8 horas
- **Testes**: 2 horas
- **Documentação**: 2 horas
- **Total**: 14 horas

---

## 🎯 Conclusão

O **Sistema de Gestão Funerária** representa uma solução completa e moderna para o gerenciamento de funerárias. Com arquitetura robusta, interface intuitiva e funcionalidades abrangentes, o sistema atende a todas as necessidades operacionais do setor.

### Principais Benefícios
- **Eficiência Operacional**: Automatização de processos
- **Controle Total**: Visibilidade completa das operações
- **Segurança**: Auditoria e controle de acesso
- **Escalabilidade**: Arquitetura preparada para crescimento
- **Manutenibilidade**: Código limpo e bem documentado

### Próximos Passos Recomendados
1. **Treinamento**: Capacitar usuários no sistema
2. **Customização**: Ajustar às necessidades específicas
3. **Integração**: Conectar com sistemas existentes
4. **Monitoramento**: Acompanhar performance e uso
5. **Evolução**: Implementar melhorias contínuas

**Sistema desenvolvido com Django seguindo as melhores práticas de desenvolvimento web.**

---

*Documentação gerada em: 31 de Agosto de 2025*  
*Versão do Sistema: 1.0.0*  
*Framework: Django 5.2.5*

