# Guia de Entrega para o Cliente

## Projeto: Chatbot WhatsApp Business para E-commerce

**Versao:** 1.0.0
**Data:** Fevereiro 2026
**Desenvolvedor:** Caio
**Stack:** Python 3.12 + FastAPI + PostgreSQL + Redis

---

## O QUE ESTA SENDO ENTREGUE

### Arquivos do Projeto

```
whatsapp-ecommerce-bot/
├── src/                          # Codigo fonte
│   ├── domain/                   # Entidades e regras de negocio
│   ├── application/              # Casos de uso
│   ├── infrastructure/           # Banco de dados, WhatsApp, Redis
│   ├── presentation/             # API REST e webhooks
│   ├── config/                   # Configuracoes
│   └── shared/                   # Utilitarios compartilhados
├── tests/                        # Testes automatizados
├── docs/                         # Documentacao
│   ├── GUIA_COMPLETO_PROJETO.md  # Explicacao didatica de tudo
│   ├── GUIA_TESTE_WHATSAPP.md    # Como testar no WhatsApp real
│   ├── PROVA_30_QUESTOES.md      # Prova pratica
│   ├── GABARITO_PROVA.md         # Gabarito com explicacoes
│   └── ENTREGA_CLIENTE.md        # Este documento
├── docker/                       # Docker Compose
├── alembic/                      # Migrations do banco
├── .env.example                  # Modelo de variaveis de ambiente
├── pyproject.toml                # Dependencias Python
└── README.md                     # Introducao do projeto
```

---

## FUNCIONALIDADES IMPLEMENTADAS

| Funcionalidade | Status | Descricao |
|----------------|--------|-----------|
| Menu de Boas-vindas | OK | Saudacao automatica quando usuario envia "Ola" |
| Consulta de Produtos | OK | Lista produtos por categoria |
| Status de Pedido | OK | Consulta status pelo numero do pedido |
| FAQ Automatico | OK | Perguntas frequentes pre-configuradas |
| Transferencia para Humano | OK | Sinaliza quando usuario quer atendente |
| Sessao de Conversa | OK | Mantem contexto da conversa por 24h |
| Persistencia em Banco | OK | Dados salvos no PostgreSQL |

---

## ARQUITETURA

```
┌─────────────────────────────────────────────────────────┐
│                    WHATSAPP                              │
│              (Mensagem do Usuario)                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    META CLOUD API                        │
│                 (Webhook -> Servidor)                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    FASTAPI                               │
│               (Recebe e valida)                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│               HANDLE MESSAGE USE CASE                    │
│            (Processa e gera resposta)                    │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐    ┌──────────┐
   │ Customer │    │ Session  │    │ Product  │
   │   Repo   │    │   Repo   │    │   Repo   │
   └────┬─────┘    └────┬─────┘    └────┬─────┘
        │               │               │
        └───────────────┼───────────────┘
                        ▼
              ┌──────────────────┐
              │   POSTGRESQL     │
              │   (Persistencia) │
              └──────────────────┘
```

---

## COMO FAZER DEPLOY

### Opcao 1: Railway (Recomendado - Mais Facil)

**Custo:** ~$5/mes
**Tempo:** ~15 minutos

1. Crie conta em https://railway.app
2. Conecte seu repositorio GitHub
3. Railway detecta automaticamente que e Python
4. Adicione servico PostgreSQL
5. Adicione servico Redis
6. Configure variaveis de ambiente (copie do .env)
7. Deploy automatico!

**Variaveis a configurar no Railway:**
```
DATABASE_URL=postgresql://... (Railway fornece)
REDIS_URL=redis://... (Railway fornece)
WHATSAPP_API_TOKEN=seu_token
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id
WHATSAPP_VERIFY_TOKEN=seu_verify_token
SECRET_KEY=chave_secreta_aleatoria
APP_ENV=production
DEBUG=false
```

### Opcao 2: Render

**Custo:** ~$7/mes
**Tempo:** ~20 minutos

1. Crie conta em https://render.com
2. Crie "Web Service" a partir do GitHub
3. Adicione PostgreSQL como servico
4. Adicione Redis como servico
5. Configure variaveis de ambiente
6. Deploy!

### Opcao 3: VPS (DigitalOcean, Vultr, etc)

**Custo:** ~$5-10/mes
**Tempo:** ~1 hora
**Requisitos:** Conhecimento de Linux

```bash
# No servidor Ubuntu 22.04
sudo apt update
sudo apt install docker.io docker-compose

# Clone o repositorio
git clone https://github.com/seu-usuario/whatsapp-bot.git
cd whatsapp-bot

# Configure o .env
cp .env.example .env
nano .env  # Edite com seus valores

# Suba os containers
docker-compose up -d

# Verifique se esta rodando
docker-compose ps
curl http://localhost:8000/health
```

---

## CONFIGURACAO DO WHATSAPP

### 1. Criar App no Meta Developers

1. Acesse https://developers.facebook.com
2. Crie um novo App tipo "Business"
3. Adicione o produto "WhatsApp"
4. Copie os tokens

### 2. Configurar Webhook

No Meta Developers:
- **URL do Webhook:** `https://seu-dominio.com/webhook`
- **Verify Token:** O mesmo que esta no .env
- **Campos:** messages, message_deliveries, message_reads

### 3. Numero de Telefone

- Use o numero de teste fornecido pelo Meta (gratuito)
- Ou adicione seu proprio numero de telefone Business

---

## CUSTOS ESTIMADOS

| Item | Custo Mensal |
|------|--------------|
| Hospedagem (Railway/Render) | $5-10 |
| WhatsApp Business API | Gratuito* |
| Dominio (opcional) | $1/mes |
| **TOTAL** | **~$6-11/mes** |

*WhatsApp Business API e gratuito para mensagens de resposta (dentro de 24h).
Mensagens iniciadas pelo bot (fora da janela) tem custo.

---

## MANUTENCAO

### Logs

```bash
# Ver logs em tempo real
docker-compose logs -f app

# Ver ultimos 100 logs
docker-compose logs --tail=100 app
```

### Banco de Dados

```bash
# Backup do banco
docker-compose exec db pg_dump -U user chatbot_db > backup.sql

# Restaurar backup
docker-compose exec -T db psql -U user chatbot_db < backup.sql
```

### Atualizacoes

```bash
# Puxar atualizacoes do GitHub
git pull origin main

# Reconstruir e reiniciar
docker-compose up -d --build
```

---

## EXPANDINDO O BOT

### Adicionar Novas Intencoes

Edite `src/application/usecases/handle_message.py`:

```python
self._intent_keywords = {
    # ... intencoes existentes ...
    "promocao": ["promocao", "desconto", "oferta", "cupom"],
}
```

### Adicionar Novas Respostas

Adicione metodo no mesmo arquivo:

```python
async def _handle_promocao(self, session: Session) -> MessageResponseDTO:
    return MessageResponseDTO(
        text="Nossas promocoes da semana:\n- 10% OFF em tudo\n- Frete gratis acima de R$100"
    )
```

### Integrar com E-commerce Real

Substitua os repositorios mock por chamadas a API do seu e-commerce:

```python
# src/infrastructure/ecommerce/client.py
class EcommerceClient:
    async def get_products(self) -> list[Product]:
        response = await self._http.get("https://sua-loja.com/api/products")
        return [Product(**p) for p in response.json()]
```

---

## SUPORTE

### Documentacao Inclusa

1. **GUIA_COMPLETO_PROJETO.md** - Explicacao completa de como tudo funciona
2. **GUIA_TESTE_WHATSAPP.md** - Passo a passo para testar
3. **PROVA_30_QUESTOES.md** - Para validar conhecimento
4. **GABARITO_PROVA.md** - Respostas com explicacoes

### Problemas Comuns

| Problema | Solucao |
|----------|---------|
| Token expirado (401) | Gerar novo token no Meta Developers |
| Webhook nao recebe | Verificar URL e verify_token |
| Banco nao conecta | Verificar DATABASE_URL |
| Mensagem nao envia | Verificar WHATSAPP_API_TOKEN |

---

## CHECKLIST DE ENTREGA

```
[x] Codigo fonte completo
[x] Testes funcionando
[x] Docker configurado
[x] Documentacao completa
[x] Guia de deploy
[x] Variaveis de ambiente documentadas
[x] Chatbot testado e funcionando
```

---

## PROXIMOS PASSOS SUGERIDOS

1. **Curto prazo (1-2 semanas)**
   - Fazer deploy em producao
   - Conectar numero real do WhatsApp Business
   - Adicionar produtos reais ao banco

2. **Medio prazo (1-2 meses)**
   - Integrar com sistema de e-commerce existente
   - Adicionar mais intencoes e respostas
   - Implementar metricas e dashboard

3. **Longo prazo (3-6 meses)**
   - Adicionar IA para respostas mais inteligentes
   - Implementar carrinho de compras
   - Sistema de notificacoes proativas

---

**Projeto desenvolvido seguindo Clean Architecture e boas praticas de desenvolvimento.**

