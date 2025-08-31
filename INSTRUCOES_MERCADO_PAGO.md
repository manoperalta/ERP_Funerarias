# Instruções para Configuração do Mercado Pago

## 1. Criar Conta no Mercado Pago

1. Acesse [https://www.mercadopago.com.br/developers](https://www.mercadopago.com.br/developers)
2. Crie uma conta ou faça login
3. Acesse "Suas integrações" > "Criar aplicação"
4. Escolha "Pagamentos online" como tipo de produto
5. Preencha os dados da aplicação

## 2. Obter Credenciais

### Credenciais de Teste (Sandbox):
- **Public Key**: Começa com `TEST-`
- **Access Token**: Começa com `TEST-`

### Credenciais de Produção:
- **Public Key**: Começa com `APP_USR-`
- **Access Token**: Começa com `APP_USR-`

## 3. Configurar no Django

Edite o arquivo `app/settings.py` e substitua as seguintes configurações:

```python
# Configurações do Mercado Pago
MERCADO_PAGO_PUBLIC_KEY = 'SUA_PUBLIC_KEY_AQUI'
MERCADO_PAGO_ACCESS_TOKEN = 'SEU_ACCESS_TOKEN_AQUI'
MERCADO_PAGO_SANDBOX = True  # False para produção
BASE_URL = 'https://seusite.com'  # URL do seu site
```

## 4. Configurar URLs de Retorno

No painel do Mercado Pago, configure as seguintes URLs de retorno:

- **Success URL**: `https://seusite.com/compra-servicos/pagamento/sucesso/{id}/`
- **Failure URL**: `https://seusite.com/compra-servicos/pagamento/falha/{id}/`
- **Pending URL**: `https://seusite.com/compra-servicos/pagamento/pendente/{id}/`

## 5. Configurar Webhook

Configure a URL do webhook para receber notificações:

- **Webhook URL**: `https://seusite.com/compra-servicos/webhook/mercado-pago/`

## 6. Testar Integração

### Cartões de Teste:

**Cartão Aprovado:**
- Número: 4509 9535 6623 3704
- CVV: 123
- Vencimento: 11/25

**Cartão Rejeitado:**
- Número: 4013 5406 8274 6260
- CVV: 123
- Vencimento: 11/25

### Usuários de Teste:

Crie usuários de teste no painel do Mercado Pago para simular compradores e vendedores.

## 7. Fluxo de Pagamento

1. Cliente adiciona itens ao carrinho
2. Cliente finaliza pedido escolhendo "Mercado Pago"
3. Sistema cria preferência de pagamento
4. Cliente é redirecionado para o Mercado Pago
5. Cliente realiza pagamento
6. Mercado Pago redireciona de volta ao site
7. Webhook atualiza status do pedido automaticamente

## 8. Status dos Pedidos

- **Pendente**: Pagamento em análise
- **Confirmado**: Pagamento aprovado
- **Cancelado**: Pagamento rejeitado

## 9. Segurança

- **NUNCA** exponha suas credenciais no código
- Use variáveis de ambiente em produção
- Configure HTTPS obrigatório
- Valide sempre os webhooks

## 10. Suporte

- Documentação: [https://www.mercadopago.com.br/developers/pt/docs](https://www.mercadopago.com.br/developers/pt/docs)
- Suporte: [https://www.mercadopago.com.br/ajuda](https://www.mercadopago.com.br/ajuda)

