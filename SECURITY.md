# Politica de Seguranca

## Vulnerabilidades Reportadas

Se voce encontrar uma vulnerabilidade de seguranca, por favor:

1. **NAO** abra uma issue publica
2. Envie email para: [seu-email@exemplo.com]
3. Inclua detalhes da vulnerabilidade
4. Aguarde resposta antes de divulgar

## Configuracoes de Seguranca Obrigatorias

### Producao

```env
# OBRIGATORIO em producao
APP_ENV=production
DEBUG=false

# Chave secreta forte (minimo 32 caracteres)
SECRET_KEY=sua-chave-super-secreta-com-minimo-32-chars

# Webhook secret do WhatsApp (obrigatorio!)
WHATSAPP_WEBHOOK_SECRET=seu-webhook-secret
```

### Checklist de Deploy

- [ ] `DEBUG=false`
- [ ] `APP_ENV=production`
- [ ] `SECRET_KEY` com minimo 32 caracteres
- [ ] `WHATSAPP_WEBHOOK_SECRET` configurado
- [ ] HTTPS habilitado
- [ ] Firewall configurado
- [ ] Logs sem dados sensiveis
- [ ] .env NAO commitado

## Arquivos Sensiveis (NUNCA commitar!)

```
.env                    # Variaveis de ambiente
*.key                   # Chaves privadas
*.pem                   # Certificados
credentials.json        # Credenciais
auth_info/              # Sessao WhatsApp
.claude/                # Configuracoes locais
```

## Vulnerabilidades Conhecidas e Mitigacoes

| Vulnerabilidade | Mitigacao | Status |
|-----------------|-----------|--------|
| Webhook sem assinatura | Obrigatorio em producao | Implementado |
| CORS permissivo | Whitelist de origens | Implementado |
| Logs com dados sensiveis | Mascaramento | Implementado |
| Payload grande | Limite 100KB | Implementado |

## Contato

Mantenedor: Caio
