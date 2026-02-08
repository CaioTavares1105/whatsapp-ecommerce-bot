# WhatsApp E-commerce Chatbot

Chatbot inteligente para WhatsApp Business API, desenvolvido em Python com Clean Architecture.

**Status:** Funcionando | **Versao:** 1.0.0 | **Data:** Fevereiro 2026

---

## Funcionalidades

| Funcionalidade | Status | Descricao |
|----------------|--------|-----------|
| Menu de Boas-vindas | OK | Saudacao automatica com menu |
| Consulta de Produtos | OK | Lista produtos por categoria |
| Rastreamento de Pedidos | OK | Status do pedido por numero |
| FAQ Automatico | OK | Respostas pre-configuradas |
| Transferencia Humano | OK | Detecta quando quer atendente |
| Sessoes Persistentes | OK | Contexto mantido por 24h |

---

## Stack Tecnologica

| Tecnologia | Versao | Proposito |
|------------|--------|-----------|
| Python | 3.12+ | Linguagem principal |
| FastAPI | 0.109+ | Framework Web/API |
| PostgreSQL | 16 | Banco de dados |
| Redis | 7.x | Cache e sessoes |
| SQLAlchemy | 2.x | ORM |
| Docker | Latest | Containerizacao |
| WhatsApp Cloud API | v18.0 | Integracao WhatsApp |

---

## Inicio Rapido

### 1. Clone o repositorio

```bash
git clone https://github.com/seu-usuario/whatsapp-ecommerce-bot.git
cd whatsapp-ecommerce-bot
```

### 2. Configure variaveis de ambiente

```bash
cp .env.example .env
# Edite o .env com seus tokens do WhatsApp
```

### 3. Suba com Docker

```bash
docker-compose up -d
```

### 4. Verifique se esta rodando

```bash
curl http://localhost:8000/health
# Retorna: {"status":"healthy","app":"whatsapp-ecommerce-bot"}
```

---

## Estrutura do Projeto

```
src/
├── domain/           # Entidades e regras de negocio
│   ├── entities/     # Customer, Product, Order, Session
│   └── repositories/ # Interfaces (ABC)
├── application/      # Casos de uso
│   └── usecases/     # HandleMessageUseCase
├── infrastructure/   # Implementacoes concretas
│   ├── database/     # SQLAlchemy + PostgreSQL
│   ├── cache/        # Redis
│   └── whatsapp/     # Client da API
├── presentation/     # Camada de entrada
│   └── api/          # FastAPI routes + webhooks
├── config/           # Configuracoes (Pydantic Settings)
└── shared/           # Utilitarios compartilhados
```

---

## Comandos Uteis

```bash
# Desenvolvimento
uvicorn src.main:app --reload --port 8000

# Testes
pytest -v

# Testes com cobertura
pytest --cov=src --cov-report=html

# Docker
docker-compose up -d          # Subir
docker-compose logs -f app    # Ver logs
docker-compose down           # Parar

# Banco de dados
alembic upgrade head          # Rodar migrations
alembic revision -m "desc"    # Criar migration
```

---

## Documentacao

| Documento | Descricao |
|-----------|-----------|
| [GUIA_COMPLETO_PROJETO.md](docs/GUIA_COMPLETO_PROJETO.md) | Explicacao didatica de todo o projeto |
| [GUIA_TESTE_WHATSAPP.md](docs/GUIA_TESTE_WHATSAPP.md) | Como testar no WhatsApp real |
| [ENTREGA_CLIENTE.md](docs/ENTREGA_CLIENTE.md) | Guia de deploy e manutencao |
| [PROVA_30_QUESTOES.md](docs/PROVA_30_QUESTOES.md) | Prova pratica |
| [GABARITO_PROVA.md](docs/GABARITO_PROVA.md) | Respostas da prova |
| [CLAUDE.md](CLAUDE.md) | Contexto completo para IA |

---

## Configuracao WhatsApp

1. Crie app em https://developers.facebook.com
2. Adicione produto "WhatsApp"
3. Crie System User em https://business.facebook.com/settings
4. Gere token permanente com permissoes:
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`
5. Configure webhook: `https://seu-dominio.com/webhook`
6. Atualize `.env` com os tokens

---

## Variaveis de Ambiente

```env
# App
APP_NAME=whatsapp-ecommerce-bot
APP_ENV=production
DEBUG=false
SECRET_KEY=sua-chave-secreta

# Banco
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db

# Redis
REDIS_URL=redis://localhost:6379/0

# WhatsApp
WHATSAPP_API_TOKEN=seu_token_permanente
WHATSAPP_PHONE_NUMBER_ID=123456789
WHATSAPP_VERIFY_TOKEN=seu_verify_token
```

---

## Deploy

### Railway (Recomendado)

1. Conecte GitHub em https://railway.app
2. Adicione PostgreSQL e Redis
3. Configure variaveis de ambiente
4. Deploy automatico!

### Docker em VPS

```bash
git clone https://github.com/seu-usuario/whatsapp-bot.git
cd whatsapp-bot
cp .env.example .env
nano .env  # Configure
docker-compose up -d
```

---

## Arquitetura

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  WhatsApp   │────▶│  Meta API   │────▶│   FastAPI   │
│  (Usuario)  │     │  (Webhook)  │     │  (Servidor) │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  UseCase    │
                                        │  Handler    │
                                        └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    ▼                          ▼                          ▼
             ┌─────────────┐           ┌─────────────┐            ┌─────────────┐
             │  Customer   │           │   Session   │            │   Product   │
             │    Repo     │           │    Repo     │            │    Repo     │
             └──────┬──────┘           └──────┬──────┘            └──────┬──────┘
                    │                         │                          │
                    └─────────────────────────┼──────────────────────────┘
                                              ▼
                                       ┌─────────────┐
                                       │ PostgreSQL  │
                                       └─────────────┘
```

---

## Licenca

MIT License

---

**Desenvolvido por Caio - 2026**

Projeto criado para aprender Python, Clean Architecture e integracao com WhatsApp Business API.
