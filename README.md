# Sistema de Gestão Funerária

Sistema completo para gestão de serviços funerários desenvolvido em Django, baseado em diagrama UML fornecido.

## Características

- **Framework**: Django 5.2.5
- **Arquitetura**: Class-Based Views (CBV)
- **Interface**: Bootstrap 5.3.0 com design responsivo
- **Padrões**: PEP 8 para código Python
- **Funcionalidades**: CRUD completo para todos os módulos

## Módulos do Sistema

### 1. Funcionários
- Cadastro e gestão de funcionários da funerária
- Campos: Nome, Cargo, Telefone, Email

### 2. Famílias
- Cadastro de famílias dos falecidos
- Campos: Nome do Responsável, Grau de Parentesco, Telefone, Email, Endereço

### 3. Pessoas Falecidas
- Registro de pessoas falecidas
- Campos: Nome, Data de Falecimento, Idade no Óbito, Família (FK)

### 4. Itens de Serviço
- Catálogo de itens e serviços oferecidos
- Campos: Nome, Quantidade, Preço Unitário, Valor Total

### 5. Serviços Contratados
- Registro de serviços contratados por família
- Campos: Pessoa Falecida (FK), Item de Serviço (FK), Valor Final

### 6. Agendamentos
- Controle de agendamentos de serviços
- Campos: Pessoa Falecida (FK), Funcionário (FK), Data/Hora, Local do Velório, Localização do Sepultamento

### 7. Planejamentos
- Planejamento de serviços funerários
- Campos: Nome do Plano, Pessoa Falecida (FK), Valor Total

### 8. Financeiro
- Controle financeiro de receitas e despesas
- Campos: Pessoa Falecida (FK), Tipo, Valor, Data de Vencimento, Status, Documento CPF/RG

## Estrutura do Projeto

```
app/
├── app/                    # Configurações principais do Django
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py           # URLs principais
│   └── wsgi.py           # Configuração WSGI
├── funcionario/          # App de funcionários
├── familia/              # App de famílias
├── pessoa_falecida/      # App de pessoas falecidas
├── item_servico/         # App de itens de serviço
├── servico_contratado/   # App de serviços contratados
├── agendamento/          # App de agendamentos
├── planejamento/         # App de planejamentos
├── financeiro/           # App financeiro
├── templates/            # Templates HTML
│   ├── base.html        # Template base
│   └── [app]/           # Templates específicos por app
├── manage.py            # Script de gerenciamento Django
└── README.md           # Este arquivo
```

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se usando git
   git clone [url-do-repositorio]
   cd app
   ```

2. **Instale as dependências**
   ```bash
   pip install django
   ```

3. **Execute as migrações do banco de dados**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Crie um superusuário (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Execute o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

6. **Acesse o sistema**
   - Abra seu navegador e acesse: `http://localhost:8000`
   - Para acessar o admin: `http://localhost:8000/admin`

## Funcionalidades Implementadas

### ✅ CRUD Completo
- **Create**: Criação de novos registros
- **Read**: Listagem e visualização de detalhes
- **Update**: Edição de registros existentes
- **Delete**: Exclusão com confirmação

### ✅ Interface de Usuário
- Design responsivo com Bootstrap 5
- Navegação intuitiva com sidebar
- Dashboard com cards informativos
- Formulários com validação
- Mensagens de feedback

### ✅ Relacionamentos
- Foreign Keys entre modelos relacionados
- Integridade referencial
- Cascata de exclusão configurada

### ✅ Validações
- Validação de formulários
- Proteção CSRF
- Validação de tipos de dados

## Tecnologias Utilizadas

- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0
- **Banco de Dados**: SQLite (padrão Django)
- **Icons**: Bootstrap Icons
- **Arquitetura**: MVT (Model-View-Template)

## Padrões de Desenvolvimento

- **PEP 8**: Código Python seguindo padrões oficiais
- **Class-Based Views**: Uso de CBVs para reutilização de código
- **Template Inheritance**: Herança de templates para consistência
- **URL Namespacing**: Organização de URLs por app
- **Separation of Concerns**: Separação clara entre lógica, apresentação e dados

## Estrutura de URLs

```
/                          # Dashboard principal
/admin/                    # Interface administrativa Django
/funcionarios/             # Listagem de funcionários
/funcionarios/novo/        # Criar novo funcionário
/funcionarios/<id>/        # Detalhes do funcionário
/funcionarios/<id>/editar/ # Editar funcionário
/funcionarios/<id>/excluir/# Excluir funcionário
/familias/                 # Listagem de famílias
/pessoas-falecidas/        # Listagem de pessoas falecidas
/itens-servico/           # Listagem de itens de serviço
/servicos-contratados/    # Listagem de serviços contratados
/agendamentos/            # Listagem de agendamentos
/planejamentos/           # Listagem de planejamentos
/financeiro/              # Listagem de registros financeiros
```

## Próximos Passos (Melhorias Futuras)

- [ ] Implementar autenticação e autorização
- [ ] Adicionar relatórios e dashboards analíticos
- [ ] Implementar sistema de notificações
- [ ] Adicionar backup automático de dados
- [ ] Implementar API REST
- [ ] Adicionar testes automatizados
- [ ] Configurar para produção com PostgreSQL

## Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências estão instaladas
2. Certifique-se de que as migrações foram executadas
3. Verifique se o servidor está rodando na porta correta

## Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração.

---

**Desenvolvido com Django e seguindo as melhores práticas de desenvolvimento web.**

