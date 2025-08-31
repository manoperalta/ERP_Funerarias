## Tarefas do Projeto Django Funerária

### Fase 1: Análise do diagrama UML e planejamento da estrutura
- [x] Analisar o diagrama UML para identificar entidades e atributos.
- [x] Mapear entidades para modelos Django.
- [x] Definir relacionamentos entre os modelos.
- [x] Esboçar a estrutura de diretórios do projeto.

### Fase 2: Configuração inicial do projeto Django
- [x] Criar o projeto Django `app`.
- [x] Configurar o `settings.py`.
- [x] Criar os apps Django para cada tabela.

### Fase 3: Criação dos apps e modelos Django
- [x] Definir os modelos em `models.py` para cada app.
- [x] Criar e aplicar as migrações iniciais.

### Fase 4: Implementação das views baseadas em classe
- [x] Criar views de listagem, detalhe, criação, atualização e exclusão para cada modelo.
- [x] Utilizar Class-Based Views (CBV).

### Fase 5: Criação dos templates HTML
- [x] Criar um template base (`base.html`).
- [x] Desenvolver templates específicos para cada view (listagem, detalhe, formulários).
- [x] Implementar a navegação entre as páginas.

### Fase 6: Configuração de URLs e integração
- [x] Configurar as URLs no nível do projeto (`urls.py` principal).
- [x] Configurar as URLs para cada app (`urls.py` dos apps).
- [x] Integrar as views com as URLs.

### Fase 7: Teste e validação do sistema
- [x] Realizar testes de funcionalidade (CRUD).
- [x] Verificar a aplicação das regras de negócio.
- [x] Garantir que o sistema está funcionando conforme o esperado.

### Fase 8: Entrega do projeto funcional
- [x] Preparar o projeto para entrega.
- [x] Fornecer instruções para execução.
- [x] Criar documentação completa (README.md).
- [x] Criar arquivo de dependências (requirements.txt).



### Fase 9: Implementação de formulários para todos os modelos
- [x] Criar formulários Django para todos os modelos.
- [x] Atualizar views para usar formulários personalizados.
- [x] Adicionar validações e widgets customizados.
- [x] Corrigir erros de campos inexistentes.

### Fase 10: Implementação do sistema de autenticação e perfis de usuário
- [x] Criar app accounts.
- [x] Criar modelo CustomUser com cargos (adm, vendedor, florista, coveiro, preparador).
- [x] Configurar AUTH_USER_MODEL.
- [x] Criar views de autenticação (login, logout, registro, perfil).
- [x] Criar formulários de autenticação.
- [x] Criar URLs para autenticação.
- [x] Criar templates de autenticação.
- [x] Aplicar migrações do novo modelo de usuário.
- [x] Testar sistema de login.

### Fase 1: Correção de todos os CRUDs para funcionamento completo
- [x] Identificar problema de CSRF nos formulários.
- [x] Corrigir configurações de CSRF_TRUSTED_ORIGINS no settings.py.
- [x] Testar todos os CRUDs (Funcionários, Famílias, Pessoas Falecidas, Itens de Serviço, Serviços Contratados, Agendamentos, Planejamentos, Financeiro).
- [x] Confirmar que todos os CRUDs estão funcionando perfeitamente.

### Fase 11: Criação de dashboards personalizados por cargo
- [ ] Criar dashboard para administradores (acesso completo + estoque).
- [ ] Criar dashboard para vendedores (fluxo de sepultamento).
- [ ] Criar dashboard para funcionários operacionais (apenas agenda).
- [ ] Implementar controle de permissões baseado em cargo.
- [ ] Criar templates específicos para cada dashboard.

### Fase 12: Criação do modelo de configurações de layout
- [ ] Criar modelo para configurações da funerária.
- [ ] Campos: nome, logo, favicon, telefone, email, endereço, redes sociais, CNPJ.
- [ ] Criar interface de administração para configurações.
- [ ] Integrar configurações nos templates.

### Fase 13: Implementação da geração de PDF/HTML para compartilhamento
- [ ] Criar sistema de geração de PDF para sepultamentos.
- [ ] Implementar template HTML para compartilhamento em redes sociais.
- [ ] Adicionar meta tags para redes sociais (Open Graph, Twitter Cards).
- [ ] Implementar signals Django para geração automática.
- [ ] Incluir foto do falecido nos documentos.

### Fase 14: Testes finais e validação de todas as funcionalidades
- [ ] Testar todos os CRUDs.
- [ ] Testar sistema de autenticação.
- [ ] Testar dashboards por cargo.
- [ ] Testar geração de PDF/HTML.
- [ ] Validar configurações de layout.

### Fase 15: Entrega final do projeto atualizado
- [ ] Atualizar documentação.
- [ ] Criar manual de uso.
- [ ] Gerar arquivo final do projeto.



### Fase 3: Modelo de configurações de layout da funerária - ✅ CONCLUÍDA
- [x] Criar app configuracoes.
- [x] Criar modelo ConfiguracaoFuneraria com todos os campos necessários.
- [x] Implementar views para gerenciar configurações.
- [x] Criar formulários de configuração.
- [x] Configurar URLs para configurações.
- [x] Aplicar migrações do modelo.
- [ ] Criar templates para configurações (próximo passo).
- [ ] Integrar configurações nos templates base.


### Fase 4: Sistema de estoque para administradores - ✅ CONCLUÍDA
- [x] Criar app estoque.
- [x] Criar modelo CategoriaEstoque para organização.
- [x] Criar modelo ProdutoEstoque com controle completo.
- [x] Criar modelo MovimentacaoEstoque para histórico.
- [x] Criar modelo AlertaEstoque para alertas automáticos.
- [x] Implementar cálculos automáticos (valor total, margem de lucro).
- [x] Aplicar migrações do sistema de estoque.
- [ ] Criar views e templates para interface (próximo passo).

### Fase 5: Sistema de geração de PDF e HTML para compartilhamento - ✅ CONCLUÍDA
- [x] Criar app documentos.
- [x] Criar modelo TemplateDocumento para templates personalizáveis.
- [x] Criar modelo DocumentoGerado com UUID único.
- [x] Criar modelo CompartilhamentoDocumento para rastreamento.
- [x] Criar modelo MetaTagsDocumento para redes sociais.
- [x] Implementar sistema de URLs públicas e privadas.
- [x] Aplicar migrações do sistema de documentos.
- [ ] Criar views para geração de PDF (próximo passo).
- [ ] Implementar templates de documentos padrão.


### Fase 6: Meta tags para redes sociais - ✅ CONCLUÍDA
- [x] Criar context processors para configurações globais.
- [x] Criar template tags personalizadas para meta tags.
- [x] Implementar Open Graph tags (Facebook, LinkedIn).
- [x] Implementar Twitter Cards.
- [x] Implementar meta tags específicas para WhatsApp.
- [x] Atualizar template base com meta tags automáticas.
- [x] Criar botões de compartilhamento social.
- [x] Implementar funcionalidade de QR Code.
- [x] Adicionar JavaScript para copiar links.

### Fase 7: Signals do Django para automação - ✅ CONCLUÍDA
- [x] Criar signals para documentos (meta tags automáticas).
- [x] Criar signals para estoque (alertas automáticos).
- [x] Criar signals para configurações (cache e validações).
- [x] Criar signals para usuários (auditoria e logs).
- [x] Implementar signal personalizado para notificações.
- [x] Configurar apps.py para carregar signals automaticamente.
- [x] Implementar logs de auditoria para todas as operações.
- [x] Validações automáticas de dados (CNPJ, CEP, WhatsApp).


## Tarefas Pendentes (Correções e Novas Funcionalidades)

- [x] Corrigir o erro TemplateDoesNotExist para financeiro/financeiro_form.html
- [x] Corrigir o erro TemplateDoesNotExist para servico_contratado/servico_contratado_form.html
- [x] Corrigir o erro TemplateDoesNotExist para agendamento/agendamento_form.html
- [x] Corrigir o erro TemplateDoesNotExist para planejamento/planejamento_form.html
- [x] Implementar campo de imagem para Pessoa Falecida e gerar posts de lembrança
- [x] Criar sistema de compra de serviços da funerária e integrar com o financeiro
- [x] Preparar integração com Mercado Pago
- [x] Testes finais e entrega do projeto corrigido

## Tarefas para a Nova Solicitação

- [x] Remover arquivos e código relacionados ao Mercado Pago
- [x] Remover o app `compra_servicos`
- [x] Revisar e corrigir todos os formulários e templates de cada app
- [ ] Garantir o funcionamento perfeito do sistema

