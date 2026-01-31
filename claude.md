# 🤖 Projeto: Chatbot WhatsApp Business para E-commerce

## 📋 Documento de Contexto para IA Assistente (Claude)

**Versão:** 1.0.0  
**Data de Criação:** Janeiro 2026  
**Autor:** Caio (Desenvolvedor)  
**Linguagem:** Python 3.12+

---

## ⚠️ REGRAS ANTI-ALUCINAÇÃO OBRIGATÓRIAS

Antes de qualquer ação, a IA assistente DEVE seguir estas regras:

### Regras de Validação

1. **NUNCA assumir que algo funciona** - Sempre testar antes de confirmar
2. **NUNCA inventar APIs ou métodos** - Sempre verificar documentação oficial
3. **NUNCA pular etapas** - Executar uma fase por vez
4. **SEMPRE mostrar fontes** - Links para documentação oficial
5. **SEMPRE pedir confirmação** - Antes de avançar para próxima fase
6. **SEMPRE explicar o "porquê"** - Justificar cada decisão técnica

### Checklist Antes de Cada Resposta

```
[ ] Verifiquei se a biblioteca existe e está atualizada no PyPI?
[ ] Confirmei a sintaxe na documentação oficial?
[ ] O código foi testado ou é testável?
[ ] Expliquei o que estou fazendo e por quê?
[ ] Pedi permissão antes de avançar?
```

---

## 🎯 Visão Geral do Projeto

### Objetivo
Criar um chatbot funcional para WhatsApp Business API que atenda clientes de um e-commerce, respondendo dúvidas sobre produtos, status de pedidos, e direcionando para atendimento humano quando necessário.

### Escopo do MVP (Minimum Viable Product)

| Funcionalidade | Prioridade | Status |
|----------------|------------|--------|
| Saudação e menu inicial | P0 | ⬜ Pendente |
| Consulta de produtos | P0 | ⬜ Pendente |
| Status de pedido | P0 | ⬜ Pendente |
| FAQ automático | P1 | ⬜ Pendente |
| Transferência para humano | P1 | ⬜ Pendente |
| Carrinho abandonado | P2 | ⬜ Pendente |

---

## 🛠️ Stack Tecnológica Definida

### Stack Principal (Validada e Atualizada)

| Tecnologia | Versão | Propósito | Documentação Oficial |
|------------|--------|-----------|---------------------|
| **Python** | 3.12+ | Linguagem | https://docs.python.org/3.12/ |
| **FastAPI** | 0.109+ | Framework Web/API | https://fastapi.tiangolo.com/ |
| **Pydantic** | 2.x | Validação de dados | https://docs.pydantic.dev/latest/ |
| **SQLAlchemy** | 2.x | ORM | https://docs.sqlalchemy.org/en/20/ |
| **Alembic** | 1.13+ | Migrations | https://alembic.sqlalchemy.org/ |
| **PostgreSQL** | 16 | Banco de dados | https://www.postgresql.org/docs/16/ |
| **Redis** | 7.x | Cache e sessões | https://redis.io/docs/ |
| **pytest** | 8.x | Testes | https://docs.pytest.org/ |
| **Docker** | Latest | Containerização | https://docs.docker.com/ |
| **UV** | Latest | Gerenciador de pacotes | https://docs.astral.sh/uv/ |

### Bibliotecas WhatsApp

| Biblioteca | Propósito | Documentação |
|------------|-----------|--------------|
| **whatsapp-web.py** | Cliente WhatsApp Web (não-oficial) | https://github.com/nicholaschum/whatsapp-web.py |
| **WhatsApp Cloud API** | API oficial Meta (recomendado) | https://developers.facebook.com/docs/whatsapp/cloud-api |

> **NOTA IMPORTANTE:** Para uso comercial em produção, recomendo fortemente usar a WhatsApp Business API oficial da Meta. As bibliotecas não-oficiais podem violar os termos de serviço do WhatsApp.

### Por que Python?

1. **Sintaxe clara** - Mais fácil de aprender e manter
2. **Ecossistema rico** - Muitas bibliotecas para automação
3. **FastAPI** - Framework moderno, rápido e com documentação automática
4. **Type hints** - Tipagem opcional mas recomendada (similar ao TypeScript)
5. **Sua experiência** - Você já trabalha com Python!

---

## 🏗️ Arquitetura do Sistema

### Padrão: Clean Architecture + DDD (Domain-Driven Design)

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  WhatsApp   │  │   REST API  │  │      Webhook Handler    │  │
│  │  Handler    │  │  (FastAPI)  │  │                         │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘  │
└─────────┼────────────────┼──────────────────────┼───────────────┘
          │                │                      │
          ▼                ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                        Use Cases                             ││
│  │  • HandleMessageUseCase                                     ││
│  │  • GetProductsUseCase                                       ││
│  │  • GetOrderStatusUseCase                                    ││
│  │  • TransferToHumanUseCase                                   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DOMAIN LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Entities   │  │   Services   │  │     Repositories     │   │
│  │  • Customer  │  │  • Message   │  │    (Interfaces)      │   │
│  │  • Product   │  │  • Chatbot   │  │                      │   │
│  │  • Order     │  │  • Session   │  │                      │   │
│  │  • Session   │  │              │  │                      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Database   │  │    Cache     │  │  External Services   │   │
│  │ (SQLAlchemy/ │  │   (Redis)    │  │  • WhatsApp API      │   │
│  │  PostgreSQL) │  │              │  │  • E-commerce API    │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Estrutura de Pastas

```
whatsapp-ecommerce-bot/
├── src/
│   ├── __init__.py
│   │
│   ├── domain/                    # Camada de Domínio
│   │   ├── __init__.py
│   │   ├── entities/              # Entidades do negócio
│   │   │   ├── __init__.py
│   │   │   ├── customer.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   └── session.py
│   │   ├── repositories/          # Interfaces (ABCs) dos repositórios
│   │   │   ├── __init__.py
│   │   │   ├── customer_repository.py
│   │   │   ├── product_repository.py
│   │   │   └── order_repository.py
│   │   └── services/              # Serviços de domínio
│   │       ├── __init__.py
│   │       └── message_service.py
│   │
│   ├── application/               # Camada de Aplicação
│   │   ├── __init__.py
│   │   ├── usecases/              # Casos de uso
│   │   │   ├── __init__.py
│   │   │   ├── handle_message.py
│   │   │   ├── get_products.py
│   │   │   └── get_order_status.py
│   │   └── dtos/                  # Data Transfer Objects
│   │       ├── __init__.py
│   │       └── message_dto.py
│   │
│   ├── infrastructure/            # Camada de Infraestrutura
│   │   ├── __init__.py
│   │   ├── database/              # Implementações de banco
│   │   │   ├── __init__.py
│   │   │   ├── connection.py      # Conexão SQLAlchemy
│   │   │   ├── models.py          # Modelos SQLAlchemy
│   │   │   └── repositories/      # Implementações concretas
│   │   │       ├── __init__.py
│   │   │       ├── sqlalchemy_customer_repo.py
│   │   │       └── sqlalchemy_product_repo.py
│   │   ├── cache/                 # Implementação Redis
│   │   │   ├── __init__.py
│   │   │   └── redis_session_store.py
│   │   └── whatsapp/              # Integração WhatsApp
│   │       ├── __init__.py
│   │       ├── client.py          # Cliente WhatsApp
│   │       └── message_handler.py
│   │
│   ├── presentation/              # Camada de Apresentação
│   │   ├── __init__.py
│   │   ├── api/                   # REST API (FastAPI)
│   │   │   ├── __init__.py
│   │   │   ├── main.py            # App FastAPI
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── products.py
│   │   │   │   └── webhooks.py
│   │   │   └── dependencies.py    # Injeção de dependência
│   │   └── whatsapp/              # Handlers WhatsApp
│   │       ├── __init__.py
│   │       └── controller.py
│   │
│   ├── config/                    # Configurações
│   │   ├── __init__.py
│   │   ├── settings.py            # Pydantic Settings
│   │   └── logging_config.py
│   │
│   └── shared/                    # Código compartilhado
│       ├── __init__.py
│       ├── errors/                # Classes de erro
│       │   ├── __init__.py
│       │   └── exceptions.py
│       ├── utils/                 # Utilitários
│       │   ├── __init__.py
│       │   └── validators.py
│       └── types/                 # Tipos globais
│           ├── __init__.py
│           └── enums.py
│
├── tests/                         # Testes
│   ├── __init__.py
│   ├── conftest.py                # Fixtures pytest
│   ├── unit/                      # Testes unitários
│   │   ├── __init__.py
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/               # Testes de integração
│   │   └── __init__.py
│   └── e2e/                       # Testes end-to-end
│       └── __init__.py
│
├── alembic/                       # Migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
│
├── docs/                          # Documentação
│   ├── api/                       # Documentação da API
│   └── architecture/              # Diagramas
│
├── docker/                        # Arquivos Docker
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .github/                       # GitHub Actions
│   └── workflows/
│       └── ci.yml
│
├── .env.example                   # Exemplo de variáveis
├── .gitignore
├── .python-version                # Versão Python (pyenv)
├── pyproject.toml                 # Configuração do projeto
├── uv.lock                        # Lock file do UV
└── README.md
```

---

## 🔐 Segurança (OBRIGATÓRIO)

### Proteções Implementadas

#### 1. Validação de Entrada
```python
# Todas as mensagens devem ser validadas com Pydantic
# NUNCA confiar em input do usuário
from pydantic import BaseModel, validator

class MessageInput(BaseModel):
    phone_number: str
    text: str
    
    @validator('text')
    def sanitize_text(cls, v):
        # Sanitização aqui
        return v.strip()
```

#### 2. Rate Limiting
- Máximo 20 mensagens por minuto por usuário
- Usar `slowapi` para rate limiting no FastAPI
- Bloqueio temporário após exceder limite

#### 3. Autenticação de Webhooks
- Verificação de assinatura em todas as requisições
- Tokens JWT para API interna

#### 4. Proteção contra Injeção
- Uso de ORM (SQLAlchemy) - previne SQL Injection
- Sanitização de mensagens com `bleach` - previne XSS

#### 5. Logs de Auditoria
- Usar `structlog` para logging estruturado
- Registro de todas as interações
- Monitoramento de tentativas suspeitas

### Checklist de Segurança

```
[ ] Variáveis de ambiente protegidas (nunca no código)
[ ] HTTPS obrigatório
[ ] Validação de webhook signatures
[ ] Rate limiting implementado
[ ] Sanitização de inputs
[ ] Logs de auditoria ativos
[ ] Backup automático do banco
```

---

## 📝 Fluxo de Conversação do Chatbot

### Fluxo Principal

```
┌─────────────────┐
│  Usuário envia  │
│    mensagem     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Identificar    │
│    sessão       │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Sessão  │
    │ existe? │
    └────┬────┘
         │
    ┌────┴────┐
   Não       Sim
    │         │
    ▼         ▼
┌───────┐ ┌────────────┐
│ Criar │ │ Recuperar  │
│sessão │ │  contexto  │
└───┬───┘ └─────┬──────┘
    │           │
    └─────┬─────┘
          │
          ▼
┌─────────────────┐
│   Processar     │
│   mensagem      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Identificar    │
│   intenção      │
└────────┬────────┘
         │
    ┌────┴────────────┬─────────────────┬────────────────┐
    │                 │                 │                │
    ▼                 ▼                 ▼                ▼
┌────────┐      ┌──────────┐     ┌──────────┐    ┌─────────┐
│Produtos│      │  Pedido  │     │   FAQ    │    │ Humano  │
└────────┘      └──────────┘     └──────────┘    └─────────┘
```

### Intenções Mapeadas

| Intenção | Palavras-chave | Resposta |
|----------|----------------|----------|
| GREETING | oi, olá, bom dia | Menu principal |
| PRODUCTS | produtos, catálogo, comprar | Lista de categorias |
| ORDER_STATUS | pedido, rastreio, onde está | Solicita número do pedido |
| FAQ | dúvida, ajuda, como funciona | Menu de perguntas frequentes |
| HUMAN | atendente, pessoa, humano | Transfere para atendimento |
| UNKNOWN | - | Mensagem de não entendimento |

---

## 🚀 FASES DE DESENVOLVIMENTO (PASSO A PASSO)

### ⚠️ REGRA: Uma fase por vez!

A IA assistente DEVE:
1. Completar uma fase inteira
2. Rodar os testes da fase
3. Mostrar resultado dos testes
4. PEDIR PERMISSÃO para avançar
5. Só então ir para próxima fase

---

## 📦 FASE 0: Setup do Ambiente e Git

### Objetivo
Configurar o ambiente de desenvolvimento Python e ensinar comandos Git essenciais.

### Pré-requisitos

Instalar no seu sistema:
1. **Python 3.12+** - https://www.python.org/downloads/
2. **UV** (gerenciador de pacotes moderno) - https://docs.astral.sh/uv/
3. **Git** - https://git-scm.com/downloads
4. **Docker Desktop** - https://www.docker.com/products/docker-desktop/

### Comandos Git Essenciais

```bash
# ===== CONFIGURAÇÃO INICIAL =====

# Configurar identidade (fazer uma vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Criar novo repositório
git init

# Clonar repositório existente
git clone https://github.com/usuario/repositorio.git

# ===== COMANDOS DO DIA A DIA =====

# Ver status dos arquivos
git status

# Adicionar arquivos para commit
git add .                    # Adiciona todos
git add arquivo.py          # Adiciona específico

# Fazer commit
git commit -m "descrição do que foi feito"

# Enviar para o GitHub
git push origin main

# Baixar atualizações do GitHub
git pull origin main

# ===== BRANCHES (RAMIFICAÇÕES) =====

# Criar e mudar para nova branch
git checkout -b feature/nome-da-feature

# Listar branches
git branch -a

# Mudar de branch
git checkout main

# Mesclar branch na main
git checkout main
git merge feature/nome-da-feature

# ===== COMANDOS ÚTEIS =====

# Ver histórico de commits
git log --oneline

# Desfazer alterações não commitadas
git checkout -- arquivo.py

# Ver diferenças
git diff

# Guardar alterações temporariamente
git stash
git stash pop  # recuperar
```

### Passo a Passo da Fase 0

```bash
# 1. Verificar instalações
python --version          # Deve mostrar 3.12+
uv --version             # Deve mostrar versão do UV
git --version            # Deve mostrar versão do Git

# 2. Criar pasta do projeto
mkdir whatsapp-ecommerce-bot
cd whatsapp-ecommerce-bot

# 3. Inicializar Git
git init

# 4. Criar .gitignore (conteúdo será fornecido)

# 5. Inicializar projeto Python com UV
uv init

# 6. Definir versão do Python
echo "3.12" > .python-version

# 7. Criar ambiente virtual e instalar dependências base
uv venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 8. Primeiro commit
git add .
git commit -m "chore: setup inicial do projeto"
```

### Conteúdo do .gitignore

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
ENV/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Build
dist/
build/
*.egg-info/

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# WhatsApp session
auth_info/
session/

# OS
.DS_Store
Thumbs.db

# UV
.uv/
uv.lock
```

### Teste da Fase 0

```bash
# Verificar se Git está funcionando
git status
# Esperado: "On branch main" ou similar

# Verificar Python
python --version
# Esperado: Python 3.12.x

# Verificar UV
uv --version
# Esperado: uv 0.x.x

# Verificar ambiente virtual
which python  # Linux/Mac
# Esperado: caminho para .venv/bin/python
```

### ✅ Critérios de Conclusão Fase 0

- [ ] Git inicializado
- [ ] .gitignore configurado
- [ ] pyproject.toml criado (via `uv init`)
- [ ] Ambiente virtual criado e ativado
- [ ] Primeiro commit feito
- [ ] (Opcional) Repositório criado no GitHub

---

## 📦 FASE 1: Estrutura Base e Configurações

### Objetivo
Criar a estrutura de pastas e arquivos de configuração.

### Arquivos a Criar

1. **pyproject.toml** - Configuração do projeto e dependências
2. **.env.example** - Template de variáveis
3. **src/config/settings.py** - Configuração com Pydantic
4. **Estrutura de pastas** - Conforme arquitetura

### pyproject.toml Completo

```toml
[project]
name = "whatsapp-ecommerce-bot"
version = "0.1.0"
description = "Chatbot WhatsApp para E-commerce"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    # Web Framework
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    
    # Validação e Settings
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    
    # Database
    "sqlalchemy>=2.0.25",
    "alembic>=1.13.0",
    "asyncpg>=0.29.0",  # PostgreSQL async driver
    
    # Cache
    "redis>=5.0.0",
    
    # HTTP Client
    "httpx>=0.26.0",
    
    # Segurança
    "python-jose[cryptography]>=3.3.0",  # JWT
    "passlib[bcrypt]>=1.7.4",
    "slowapi>=0.1.9",  # Rate limiting
    
    # Logging
    "structlog>=24.1.0",
    
    # Utilitários
    "python-dotenv>=1.0.0",
    "bleach>=6.1.0",  # Sanitização
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.26.0",  # Para testes de API
    "ruff>=0.1.0",  # Linter
    "mypy>=1.8.0",  # Type checking
    "pre-commit>=3.6.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --cov=src --cov-report=term-missing"

[tool.ruff]
target-version = "py312"
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Conteúdo do .env.example

```env
# App
APP_NAME=whatsapp-ecommerce-bot
APP_ENV=development
DEBUG=true
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/chatbot_db

# Redis
REDIS_URL=redis://localhost:6379/0

# WhatsApp (escolha uma opção)
# Opção 1: WhatsApp Cloud API (Oficial - Recomendado)
WHATSAPP_API_TOKEN=seu-token-aqui
WHATSAPP_PHONE_NUMBER_ID=seu-phone-id
WHATSAPP_VERIFY_TOKEN=seu-verify-token
WHATSAPP_WEBHOOK_SECRET=seu-webhook-secret

# Opção 2: Baileys/whatsapp-web.py (Não-oficial)
# WHATSAPP_SESSION_PATH=./auth_info

# API
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

### src/config/settings.py

```python
"""
Configurações da aplicação usando Pydantic Settings.
Carrega variáveis de ambiente automaticamente.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # App
    app_name: str = "whatsapp-ecommerce-bot"
    app_env: str = "development"
    debug: bool = False
    secret_key: str
    
    # Database
    database_url: str
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # WhatsApp Cloud API
    whatsapp_api_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    whatsapp_verify_token: str | None = None
    whatsapp_webhook_secret: str | None = None
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def is_production(self) -> bool:
        """Verifica se está em produção."""
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância cacheada das configurações.
    Usar @lru_cache para não recarregar .env a cada chamada.
    """
    return Settings()
```

### Passo a Passo da Fase 1

```bash
# 1. Criar estrutura de pastas
mkdir -p src/{domain/{entities,repositories,services},application/{usecases,dtos},infrastructure/{database/repositories,cache,whatsapp},presentation/{api/routes,whatsapp},config,shared/{errors,utils,types}}
mkdir -p tests/{unit/{domain,application,infrastructure},integration,e2e}
mkdir -p docs/{api,architecture}
mkdir -p docker
mkdir -p alembic/versions

# 2. Criar arquivos __init__.py em todas as pastas
find src tests -type d -exec touch {}/__init__.py \;

# 3. Copiar pyproject.toml com dependências

# 4. Copiar .env.example

# 5. Criar .env a partir do exemplo
cp .env.example .env
# Editar .env com suas configurações

# 6. Copiar src/config/settings.py

# 7. Instalar dependências
uv pip install -e ".[dev]"

# 8. Verificar se tudo foi instalado
uv pip list
```

### Teste da Fase 1

```bash
# Verificar estrutura de pastas
find src -type d | head -20

# Verificar se Python importa o módulo de configuração
python -c "from src.config.settings import get_settings; print(get_settings().app_name)"
# Esperado: whatsapp-ecommerce-bot

# Verificar dependências instaladas
python -c "import fastapi; print(fastapi.__version__)"
# Esperado: 0.109.x ou superior

# Verificar se pytest funciona
pytest --version
# Esperado: pytest 8.x.x
```

### ✅ Critérios de Conclusão Fase 1

- [ ] Todas as pastas criadas
- [ ] pyproject.toml configurado corretamente
- [ ] Dependências instaladas sem erros
- [ ] .env.example com todas as variáveis necessárias
- [ ] settings.py carregando configurações
- [ ] Python importa módulos sem erro

---

## 📦 FASE 2: Camada de Domínio (Entities)

### Objetivo
Criar as entidades de negócio com tipagem forte usando dataclasses e Pydantic.

### Conceitos Python Importantes

```python
# Dataclasses - Classes de dados simplificadas
from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Customer:
    phone_number: str
    name: str | None = None  # Opcional (Python 3.10+)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
```

### Entidades a Criar

1. **Customer** - Cliente do e-commerce
2. **Product** - Produto à venda
3. **Order** - Pedido do cliente
4. **Session** - Sessão de conversa
5. **Message** - Mensagem do chat

### src/domain/entities/customer.py

```python
"""
Entidade Customer (Cliente).
Representa um cliente do e-commerce.
"""
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Customer:
    """Entidade de domínio que representa um cliente."""
    
    phone_number: str
    name: str | None = None
    email: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validações após inicialização."""
        self._validate_phone_number()
    
    def _validate_phone_number(self) -> None:
        """Valida formato do telefone."""
        # Remove caracteres não numéricos
        clean_phone = "".join(filter(str.isdigit, self.phone_number))
        
        if len(clean_phone) < 10 or len(clean_phone) > 15:
            raise ValueError(
                f"Número de telefone inválido: {self.phone_number}. "
                "Deve ter entre 10 e 15 dígitos."
            )
        
        self.phone_number = clean_phone
    
    def update_name(self, name: str) -> None:
        """Atualiza o nome do cliente."""
        self.name = name
        self.updated_at = datetime.now()
    
    def update_email(self, email: str) -> None:
        """Atualiza o email do cliente."""
        # Validação básica de email
        if "@" not in email or "." not in email:
            raise ValueError(f"Email inválido: {email}")
        self.email = email
        self.updated_at = datetime.now()
```

### src/domain/entities/product.py

```python
"""
Entidade Product (Produto).
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
import uuid


@dataclass
class Product:
    """Entidade de domínio que representa um produto."""
    
    name: str
    price: Decimal
    category: str
    description: str | None = None
    image_url: str | None = None
    stock: int = 0
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validações após inicialização."""
        if self.price < 0:
            raise ValueError("Preço não pode ser negativo")
        if self.stock < 0:
            raise ValueError("Estoque não pode ser negativo")
    
    @property
    def is_available(self) -> bool:
        """Verifica se produto está disponível para venda."""
        return self.active and self.stock > 0
    
    def decrease_stock(self, quantity: int) -> None:
        """Diminui o estoque do produto."""
        if quantity > self.stock:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {self.stock}, "
                f"Solicitado: {quantity}"
            )
        self.stock -= quantity
        self.updated_at = datetime.now()
```

### src/shared/types/enums.py

```python
"""
Enums compartilhados do sistema.
"""
from enum import Enum


class OrderStatus(str, Enum):
    """Status possíveis de um pedido."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class SessionState(str, Enum):
    """Estados possíveis de uma sessão de chat."""
    INITIAL = "initial"
    MENU = "menu"
    PRODUCTS = "products"
    ORDER_STATUS = "order_status"
    FAQ = "faq"
    HUMAN_TRANSFER = "human_transfer"


class MessageDirection(str, Enum):
    """Direção da mensagem."""
    INCOMING = "incoming"  # Usuário -> Bot
    OUTGOING = "outgoing"  # Bot -> Usuário
```

### src/domain/entities/order.py

```python
"""
Entidade Order (Pedido).
"""
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
import uuid

from src.shared.types.enums import OrderStatus


@dataclass
class Order:
    """Entidade de domínio que representa um pedido."""
    
    customer_id: str
    total: Decimal
    status: OrderStatus = OrderStatus.PENDING
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validações após inicialização."""
        if self.total < 0:
            raise ValueError("Total não pode ser negativo")
    
    def confirm(self) -> None:
        """Confirma o pedido."""
        if self.status != OrderStatus.PENDING:
            raise ValueError(
                f"Pedido não pode ser confirmado. Status atual: {self.status}"
            )
        self.status = OrderStatus.CONFIRMED
        self.updated_at = datetime.now()
    
    def cancel(self) -> None:
        """Cancela o pedido."""
        if self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise ValueError(
                f"Pedido não pode ser cancelado. Status atual: {self.status}"
            )
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now()
    
    def ship(self) -> None:
        """Marca pedido como enviado."""
        if self.status != OrderStatus.PROCESSING:
            raise ValueError(
                f"Pedido não pode ser enviado. Status atual: {self.status}"
            )
        self.status = OrderStatus.SHIPPED
        self.updated_at = datetime.now()
```

### src/domain/entities/session.py

```python
"""
Entidade Session (Sessão de Chat).
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any
import uuid

from src.shared.types.enums import SessionState


@dataclass
class Session:
    """Entidade de domínio que representa uma sessão de chat."""
    
    customer_id: str
    state: SessionState = SessionState.INITIAL
    context: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(
        default_factory=lambda: datetime.now() + timedelta(hours=24)
    )
    
    @property
    def is_expired(self) -> bool:
        """Verifica se a sessão expirou."""
        return datetime.now() > self.expires_at
    
    def update_state(self, new_state: SessionState) -> None:
        """Atualiza o estado da sessão."""
        self.state = new_state
        self.updated_at = datetime.now()
        # Renova expiração a cada interação
        self.expires_at = datetime.now() + timedelta(hours=24)
    
    def set_context(self, key: str, value: Any) -> None:
        """Define um valor no contexto da sessão."""
        self.context[key] = value
        self.updated_at = datetime.now()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Obtém um valor do contexto da sessão."""
        return self.context.get(key, default)
    
    def clear_context(self) -> None:
        """Limpa o contexto da sessão."""
        self.context = {}
        self.updated_at = datetime.now()
```

### Teste da Fase 2

Criar arquivo: `tests/unit/domain/entities/test_customer.py`

```python
"""
Testes unitários para entidade Customer.
"""
import pytest
from src.domain.entities.customer import Customer


class TestCustomer:
    """Testes para a entidade Customer."""
    
    def test_create_customer_with_valid_phone(self):
        """Deve criar cliente com telefone válido."""
        customer = Customer(
            phone_number="5511999999999",
            name="João Silva"
        )
        
        assert customer.id is not None
        assert customer.phone_number == "5511999999999"
        assert customer.name == "João Silva"
    
    def test_create_customer_cleans_phone_number(self):
        """Deve limpar caracteres do telefone."""
        customer = Customer(
            phone_number="+55 (11) 99999-9999"
        )
        
        assert customer.phone_number == "5511999999999"
    
    def test_create_customer_with_invalid_phone_raises_error(self):
        """Deve levantar erro com telefone inválido."""
        with pytest.raises(ValueError) as exc_info:
            Customer(phone_number="123")
        
        assert "inválido" in str(exc_info.value).lower()
    
    def test_update_name(self):
        """Deve atualizar nome do cliente."""
        customer = Customer(phone_number="5511999999999")
        old_updated_at = customer.updated_at
        
        customer.update_name("Maria Silva")
        
        assert customer.name == "Maria Silva"
        assert customer.updated_at > old_updated_at
    
    def test_update_email_valid(self):
        """Deve atualizar email válido."""
        customer = Customer(phone_number="5511999999999")
        
        customer.update_email("teste@email.com")
        
        assert customer.email == "teste@email.com"
    
    def test_update_email_invalid_raises_error(self):
        """Deve levantar erro com email inválido."""
        customer = Customer(phone_number="5511999999999")
        
        with pytest.raises(ValueError) as exc_info:
            customer.update_email("email-invalido")
        
        assert "inválido" in str(exc_info.value).lower()
```

Criar arquivo: `tests/unit/domain/entities/test_product.py`

```python
"""
Testes unitários para entidade Product.
"""
import pytest
from decimal import Decimal
from src.domain.entities.product import Product


class TestProduct:
    """Testes para a entidade Product."""
    
    def test_create_product(self):
        """Deve criar produto válido."""
        product = Product(
            name="Camiseta",
            price=Decimal("49.90"),
            category="Roupas",
            stock=10
        )
        
        assert product.id is not None
        assert product.name == "Camiseta"
        assert product.price == Decimal("49.90")
        assert product.is_available is True
    
    def test_product_not_available_when_inactive(self):
        """Produto inativo não está disponível."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=10,
            active=False
        )
        
        assert product.is_available is False
    
    def test_product_not_available_when_no_stock(self):
        """Produto sem estoque não está disponível."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=0
        )
        
        assert product.is_available is False
    
    def test_decrease_stock(self):
        """Deve diminuir estoque corretamente."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=10
        )
        
        product.decrease_stock(3)
        
        assert product.stock == 7
    
    def test_decrease_stock_insufficient_raises_error(self):
        """Deve levantar erro se estoque insuficiente."""
        product = Product(
            name="Produto",
            price=Decimal("10.00"),
            category="Teste",
            stock=5
        )
        
        with pytest.raises(ValueError) as exc_info:
            product.decrease_stock(10)
        
        assert "insuficiente" in str(exc_info.value).lower()
    
    def test_negative_price_raises_error(self):
        """Preço negativo deve levantar erro."""
        with pytest.raises(ValueError):
            Product(
                name="Produto",
                price=Decimal("-10.00"),
                category="Teste"
            )
```

### Rodar Testes da Fase 2

```bash
# Rodar todos os testes
pytest tests/unit/domain/entities/ -v

# Rodar com cobertura
pytest tests/unit/domain/entities/ -v --cov=src/domain/entities

# Esperado: Todos os testes passando (verde)
```

### ✅ Critérios de Conclusão Fase 2

- [ ] Todas as entidades criadas (Customer, Product, Order, Session)
- [ ] Enums criados (OrderStatus, SessionState, MessageDirection)
- [ ] Testes unitários passando (100%)
- [ ] Tipagem Python sem erros
- [ ] Validações de domínio implementadas

---

## 📦 FASE 3: Interfaces de Repositório

### Objetivo
Definir contratos (Abstract Base Classes) para acesso a dados.

### Por que usar ABC (Abstract Base Class)?

Em Python, usamos `abc.ABC` para criar interfaces:
- Define um contrato que implementações devem seguir
- Permite injeção de dependência
- Facilita testes com mocks

### src/domain/repositories/customer_repository.py

```python
"""
Interface (ABC) para repositório de Customer.
"""
from abc import ABC, abstractmethod

from src.domain.entities.customer import Customer


class ICustomerRepository(ABC):
    """Interface para repositório de clientes."""
    
    @abstractmethod
    async def find_by_phone(self, phone: str) -> Customer | None:
        """Busca cliente por número de telefone."""
        ...
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Customer | None:
        """Busca cliente por ID."""
        ...
    
    @abstractmethod
    async def save(self, customer: Customer) -> None:
        """Salva um novo cliente."""
        ...
    
    @abstractmethod
    async def update(self, customer: Customer) -> None:
        """Atualiza um cliente existente."""
        ...
    
    @abstractmethod
    async def delete(self, id: str) -> None:
        """Remove um cliente."""
        ...
```

### src/domain/repositories/product_repository.py

```python
"""
Interface (ABC) para repositório de Product.
"""
from abc import ABC, abstractmethod

from src.domain.entities.product import Product


class IProductRepository(ABC):
    """Interface para repositório de produtos."""
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Product | None:
        """Busca produto por ID."""
        ...
    
    @abstractmethod
    async def find_by_category(self, category: str) -> list[Product]:
        """Busca produtos por categoria."""
        ...
    
    @abstractmethod
    async def find_all_active(self) -> list[Product]:
        """Lista todos os produtos ativos."""
        ...
    
    @abstractmethod
    async def search(self, query: str) -> list[Product]:
        """Busca produtos por nome ou descrição."""
        ...
    
    @abstractmethod
    async def save(self, product: Product) -> None:
        """Salva um novo produto."""
        ...
    
    @abstractmethod
    async def update(self, product: Product) -> None:
        """Atualiza um produto existente."""
        ...
```

### src/domain/repositories/order_repository.py

```python
"""
Interface (ABC) para repositório de Order.
"""
from abc import ABC, abstractmethod

from src.domain.entities.order import Order
from src.shared.types.enums import OrderStatus


class IOrderRepository(ABC):
    """Interface para repositório de pedidos."""
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Order | None:
        """Busca pedido por ID."""
        ...
    
    @abstractmethod
    async def find_by_customer(self, customer_id: str) -> list[Order]:
        """Busca pedidos de um cliente."""
        ...
    
    @abstractmethod
    async def find_by_status(self, status: OrderStatus) -> list[Order]:
        """Busca pedidos por status."""
        ...
    
    @abstractmethod
    async def save(self, order: Order) -> None:
        """Salva um novo pedido."""
        ...
    
    @abstractmethod
    async def update(self, order: Order) -> None:
        """Atualiza um pedido existente."""
        ...
```

### src/domain/repositories/session_repository.py

```python
"""
Interface (ABC) para repositório de Session.
"""
from abc import ABC, abstractmethod

from src.domain.entities.session import Session


class ISessionRepository(ABC):
    """Interface para repositório de sessões."""
    
    @abstractmethod
    async def find_by_id(self, id: str) -> Session | None:
        """Busca sessão por ID."""
        ...
    
    @abstractmethod
    async def find_by_customer(self, customer_id: str) -> Session | None:
        """Busca sessão ativa de um cliente."""
        ...
    
    @abstractmethod
    async def find_active_by_phone(self, phone: str) -> Session | None:
        """Busca sessão ativa pelo telefone do cliente."""
        ...
    
    @abstractmethod
    async def save(self, session: Session) -> None:
        """Salva uma nova sessão."""
        ...
    
    @abstractmethod
    async def update(self, session: Session) -> None:
        """Atualiza uma sessão existente."""
        ...
    
    @abstractmethod
    async def delete_expired(self) -> int:
        """Remove sessões expiradas. Retorna quantidade removida."""
        ...
```

### src/domain/repositories/__init__.py

```python
"""
Interfaces dos repositórios.
Exporta todas as interfaces para facilitar imports.
"""
from src.domain.repositories.customer_repository import ICustomerRepository
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.repositories.product_repository import IProductRepository
from src.domain.repositories.session_repository import ISessionRepository

__all__ = [
    "ICustomerRepository",
    "IOrderRepository",
    "IProductRepository",
    "ISessionRepository",
]
```

### Teste da Fase 3

```bash
# Verificar se interfaces são importáveis
python -c "from src.domain.repositories import ICustomerRepository, IProductRepository, IOrderRepository, ISessionRepository; print('OK!')"

# Verificar tipagem com mypy
mypy src/domain/repositories/
```

### ✅ Critérios de Conclusão Fase 3

- [ ] Interfaces de todos os repositórios criadas
- [ ] Todas são Abstract Base Classes (ABC)
- [ ] Métodos async definidos corretamente
- [ ] Nenhuma dependência de implementação concreta
- [ ] Import funcionando sem erros

---

## 📦 FASE 4: Casos de Uso (Application Layer)

### Objetivo
Implementar a lógica de negócio nos casos de uso.

### Casos de Uso a Implementar

1. **HandleMessageUseCase** - Processa mensagem recebida
2. **GetProductsUseCase** - Lista produtos
3. **GetOrderStatusUseCase** - Consulta status de pedido
4. **CreateSessionUseCase** - Cria nova sessão
5. **TransferToHumanUseCase** - Transfere para atendente

### src/application/dtos/message_dto.py

```python
"""
DTOs para mensagens.
"""
from pydantic import BaseModel, Field

from src.shared.types.enums import MessageDirection


class IncomingMessageDTO(BaseModel):
    """DTO para mensagem recebida do usuário."""
    phone_number: str = Field(..., min_length=10, max_length=15)
    text: str = Field(..., min_length=1)
    message_id: str | None = None


class OutgoingMessageDTO(BaseModel):
    """DTO para mensagem enviada ao usuário."""
    phone_number: str
    text: str
    direction: MessageDirection = MessageDirection.OUTGOING


class MessageResponseDTO(BaseModel):
    """DTO para resposta do processamento de mensagem."""
    text: str
    should_transfer_to_human: bool = False
    metadata: dict | None = None
```

### src/application/usecases/handle_message.py

```python
"""
Caso de uso: Processar mensagem recebida.
Este é o caso de uso principal do chatbot.
"""
from src.application.dtos.message_dto import IncomingMessageDTO, MessageResponseDTO
from src.domain.entities.customer import Customer
from src.domain.entities.session import Session
from src.domain.repositories import (
    ICustomerRepository,
    ISessionRepository,
    IProductRepository,
    IOrderRepository,
)
from src.shared.types.enums import SessionState


class HandleMessageUseCase:
    """
    Processa uma mensagem recebida do WhatsApp.
    
    Fluxo:
    1. Identifica ou cria cliente
    2. Identifica ou cria sessão
    3. Identifica intenção da mensagem
    4. Processa baseado no estado atual
    5. Retorna resposta apropriada
    """
    
    def __init__(
        self,
        customer_repo: ICustomerRepository,
        session_repo: ISessionRepository,
        product_repo: IProductRepository,
        order_repo: IOrderRepository,
    ) -> None:
        self._customer_repo = customer_repo
        self._session_repo = session_repo
        self._product_repo = product_repo
        self._order_repo = order_repo
        
        # Palavras-chave para identificar intenções
        self._intent_keywords = {
            "greeting": ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "hey", "hi"],
            "products": ["produto", "produtos", "catalogo", "catálogo", "comprar", "preço", "preco"],
            "order_status": ["pedido", "rastreio", "rastrear", "onde está", "onde esta", "entrega"],
            "faq": ["dúvida", "duvida", "ajuda", "como funciona", "informação", "informacao"],
            "human": ["atendente", "humano", "pessoa", "falar com alguém", "falar com alguem"],
            "menu": ["menu", "voltar", "início", "inicio", "opcoes", "opções"],
        }
    
    async def execute(self, input_dto: IncomingMessageDTO) -> MessageResponseDTO:
        """Executa o processamento da mensagem."""
        
        # 1. Buscar ou criar cliente
        customer = await self._get_or_create_customer(input_dto.phone_number)
        
        # 2. Buscar ou criar sessão
        session = await self._get_or_create_session(customer.id)
        
        # 3. Identificar intenção
        intent = self._identify_intent(input_dto.text)
        
        # 4. Processar baseado no estado e intenção
        response = await self._process_message(session, intent, input_dto.text)
        
        # 5. Atualizar sessão
        await self._session_repo.update(session)
        
        return response
    
    async def _get_or_create_customer(self, phone_number: str) -> Customer:
        """Busca cliente existente ou cria novo."""
        customer = await self._customer_repo.find_by_phone(phone_number)
        
        if customer is None:
            customer = Customer(phone_number=phone_number)
            await self._customer_repo.save(customer)
        
        return customer
    
    async def _get_or_create_session(self, customer_id: str) -> Session:
        """Busca sessão ativa ou cria nova."""
        session = await self._session_repo.find_by_customer(customer_id)
        
        if session is None or session.is_expired:
            session = Session(customer_id=customer_id)
            await self._session_repo.save(session)
        
        return session
    
    def _identify_intent(self, text: str) -> str:
        """Identifica a intenção da mensagem."""
        text_lower = text.lower().strip()
        
        for intent, keywords in self._intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return "unknown"
    
    async def _process_message(
        self, 
        session: Session, 
        intent: str, 
        text: str
    ) -> MessageResponseDTO:
        """Processa mensagem baseado no estado atual e intenção."""
        
        # Se pede menu ou está no início
        if intent in ["greeting", "menu"] or session.state == SessionState.INITIAL:
            return await self._handle_greeting(session)
        
        # Se quer ver produtos
        if intent == "products":
            return await self._handle_products(session)
        
        # Se quer status do pedido
        if intent == "order_status":
            return await self._handle_order_status(session, text)
        
        # Se quer FAQ
        if intent == "faq":
            return await self._handle_faq(session)
        
        # Se quer falar com humano
        if intent == "human":
            return await self._handle_human_transfer(session)
        
        # Processar baseado no estado atual
        if session.state == SessionState.ORDER_STATUS:
            return await self._process_order_number(session, text)
        
        # Não entendeu
        return await self._handle_unknown(session)
    
    async def _handle_greeting(self, session: Session) -> MessageResponseDTO:
        """Retorna saudação e menu principal."""
        session.update_state(SessionState.MENU)
        
        return MessageResponseDTO(
            text=(
                "Olá! 👋 Bem-vindo à nossa loja!\n\n"
                "Como posso ajudar você hoje?\n\n"
                "1️⃣ Ver produtos\n"
                "2️⃣ Rastrear pedido\n"
                "3️⃣ Dúvidas frequentes\n"
                "4️⃣ Falar com atendente\n\n"
                "Digite o número da opção desejada ou escreva sua dúvida."
            )
        )
    
    async def _handle_products(self, session: Session) -> MessageResponseDTO:
        """Retorna lista de produtos/categorias."""
        session.update_state(SessionState.PRODUCTS)
        
        products = await self._product_repo.find_all_active()
        
        if not products:
            return MessageResponseDTO(
                text="No momento não temos produtos disponíveis. Tente novamente mais tarde!"
            )
        
        # Agrupar por categoria
        categories: dict[str, list] = {}
        for product in products:
            if product.category not in categories:
                categories[product.category] = []
            categories[product.category].append(product)
        
        text = "📦 *Nossos Produtos*\n\n"
        for category, items in categories.items():
            text += f"*{category}:*\n"
            for item in items[:5]:  # Limita 5 por categoria
                text += f"  • {item.name} - R$ {item.price:.2f}\n"
            text += "\n"
        
        text += "Digite o nome do produto para mais detalhes ou 'menu' para voltar."
        
        return MessageResponseDTO(text=text)
    
    async def _handle_order_status(self, session: Session, text: str) -> MessageResponseDTO:
        """Inicia fluxo de rastreamento de pedido."""
        session.update_state(SessionState.ORDER_STATUS)
        
        return MessageResponseDTO(
            text=(
                "📦 *Rastrear Pedido*\n\n"
                "Por favor, digite o número do seu pedido.\n\n"
                "Exemplo: `PED-123456`"
            )
        )
    
    async def _process_order_number(self, session: Session, text: str) -> MessageResponseDTO:
        """Processa número do pedido informado."""
        # Remove espaços e converte para maiúsculo
        order_id = text.strip().upper()
        
        order = await self._order_repo.find_by_id(order_id)
        
        if order is None:
            return MessageResponseDTO(
                text=(
                    f"❌ Pedido *{order_id}* não encontrado.\n\n"
                    "Verifique o número e tente novamente, ou digite 'menu' para voltar."
                )
            )
        
        status_messages = {
            "pending": "⏳ Aguardando confirmação",
            "confirmed": "✅ Pedido confirmado",
            "processing": "📦 Em preparação",
            "shipped": "🚚 Enviado - A caminho",
            "delivered": "✅ Entregue",
            "cancelled": "❌ Cancelado",
        }
        
        status_text = status_messages.get(order.status.value, order.status.value)
        
        return MessageResponseDTO(
            text=(
                f"📦 *Pedido {order_id}*\n\n"
                f"Status: {status_text}\n"
                f"Valor: R$ {order.total:.2f}\n"
                f"Data: {order.created_at.strftime('%d/%m/%Y')}\n\n"
                "Digite 'menu' para voltar."
            )
        )
    
    async def _handle_faq(self, session: Session) -> MessageResponseDTO:
        """Retorna menu de perguntas frequentes."""
        session.update_state(SessionState.FAQ)
        
        return MessageResponseDTO(
            text=(
                "❓ *Perguntas Frequentes*\n\n"
                "1️⃣ Qual o prazo de entrega?\n"
                "2️⃣ Como faço para trocar?\n"
                "3️⃣ Quais formas de pagamento?\n"
                "4️⃣ Como cancelar um pedido?\n\n"
                "Digite o número da pergunta ou 'menu' para voltar."
            )
        )
    
    async def _handle_human_transfer(self, session: Session) -> MessageResponseDTO:
        """Transfere para atendimento humano."""
        session.update_state(SessionState.HUMAN_TRANSFER)
        
        return MessageResponseDTO(
            text=(
                "👤 *Atendimento Humano*\n\n"
                "Vou transferir você para um de nossos atendentes.\n"
                "Aguarde um momento, por favor.\n\n"
                "Horário de atendimento:\n"
                "Segunda a Sexta: 9h às 18h\n"
                "Sábado: 9h às 13h"
            ),
            should_transfer_to_human=True
        )
    
    async def _handle_unknown(self, session: Session) -> MessageResponseDTO:
        """Mensagem quando não entende a intenção."""
        return MessageResponseDTO(
            text=(
                "🤔 Desculpe, não entendi sua mensagem.\n\n"
                "Você pode:\n"
                "• Digitar 'menu' para ver as opções\n"
                "• Digitar 'atendente' para falar com uma pessoa\n"
            )
        )
```

### Teste da Fase 4

```bash
# Criar testes para o caso de uso
# tests/unit/application/usecases/test_handle_message.py
```

```python
"""
Testes para HandleMessageUseCase.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.application.dtos.message_dto import IncomingMessageDTO
from src.application.usecases.handle_message import HandleMessageUseCase
from src.domain.entities.customer import Customer
from src.domain.entities.session import Session
from src.shared.types.enums import SessionState


@pytest.fixture
def mock_repositories():
    """Fixture que cria mocks dos repositórios."""
    return {
        "customer_repo": AsyncMock(),
        "session_repo": AsyncMock(),
        "product_repo": AsyncMock(),
        "order_repo": AsyncMock(),
    }


@pytest.fixture
def use_case(mock_repositories):
    """Fixture que cria o caso de uso com mocks."""
    return HandleMessageUseCase(**mock_repositories)


class TestHandleMessageUseCase:
    """Testes para HandleMessageUseCase."""
    
    @pytest.mark.asyncio
    async def test_greeting_returns_menu(self, use_case, mock_repositories):
        """Saudação deve retornar menu principal."""
        # Arrange
        customer = Customer(phone_number="5511999999999")
        session = Session(customer_id=customer.id)
        
        mock_repositories["customer_repo"].find_by_phone.return_value = customer
        mock_repositories["session_repo"].find_by_customer.return_value = session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Olá"
        )
        
        # Act
        result = await use_case.execute(input_dto)
        
        # Assert
        assert "Bem-vindo" in result.text
        assert "1️⃣" in result.text  # Menu
        assert result.should_transfer_to_human is False
    
    @pytest.mark.asyncio
    async def test_new_customer_is_created(self, use_case, mock_repositories):
        """Novo cliente deve ser criado se não existir."""
        # Arrange
        mock_repositories["customer_repo"].find_by_phone.return_value = None
        mock_repositories["session_repo"].find_by_customer.return_value = None
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Oi"
        )
        
        # Act
        await use_case.execute(input_dto)
        
        # Assert
        mock_repositories["customer_repo"].save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_human_transfer_sets_flag(self, use_case, mock_repositories):
        """Pedido de atendente deve setar flag de transferência."""
        # Arrange
        customer = Customer(phone_number="5511999999999")
        session = Session(customer_id=customer.id)
        
        mock_repositories["customer_repo"].find_by_phone.return_value = customer
        mock_repositories["session_repo"].find_by_customer.return_value = session
        
        input_dto = IncomingMessageDTO(
            phone_number="5511999999999",
            text="Quero falar com um atendente"
        )
        
        # Act
        result = await use_case.execute(input_dto)
        
        # Assert
        assert result.should_transfer_to_human is True
        assert "Atendimento Humano" in result.text
```

### Rodar Testes da Fase 4

```bash
pytest tests/unit/application/ -v
```

### ✅ Critérios de Conclusão Fase 4

- [ ] HandleMessageUseCase implementado
- [ ] DTOs criados (IncomingMessageDTO, MessageResponseDTO)
- [ ] Testes unitários passando
- [ ] Injeção de dependência funcionando (repositórios como parâmetros)

---

## 📦 FASE 5: Infraestrutura - Banco de Dados

### Objetivo
Configurar PostgreSQL com SQLAlchemy ORM.

### Modelos SQLAlchemy

```python
# src/infrastructure/database/models.py
"""
Modelos SQLAlchemy para o banco de dados.
"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.shared.types.enums import OrderStatus, SessionState


class Base(DeclarativeBase):
    """Base para todos os modelos."""
    pass


class CustomerModel(Base):
    """Modelo de cliente no banco."""
    __tablename__ = "customers"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    
    # Relacionamentos
    orders: Mapped[list["OrderModel"]] = relationship(back_populates="customer")
    sessions: Mapped[list["SessionModel"]] = relationship(back_populates="customer")


class ProductModel(Base):
    """Modelo de produto no banco."""
    __tablename__ = "products"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    image_url: Mapped[str | None] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(100), index=True)
    stock: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )


class OrderModel(Base):
    """Modelo de pedido no banco."""
    __tablename__ = "orders"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), default=OrderStatus.PENDING
    )
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    
    # Relacionamentos
    customer: Mapped["CustomerModel"] = relationship(back_populates="orders")


class SessionModel(Base):
    """Modelo de sessão de chat no banco."""
    __tablename__ = "sessions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    state: Mapped[SessionState] = mapped_column(
        Enum(SessionState), default=SessionState.INITIAL
    )
    context: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    
    # Relacionamentos
    customer: Mapped["CustomerModel"] = relationship(back_populates="sessions")
```

### Conexão com Banco de Dados

```python
# src/infrastructure/database/connection.py
"""
Configuração da conexão com o banco de dados.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config.settings import get_settings


settings = get_settings()

# Criar engine assíncrona
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL em desenvolvimento
    pool_size=5,
    max_overflow=10,
)

# Criar factory de sessões
AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncSession:
    """
    Dependency para injetar sessão do banco.
    Usar com FastAPI Depends().
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### ✅ Critérios de Conclusão Fase 5

- [ ] Modelos SQLAlchemy criados
- [ ] Conexão async configurada
- [ ] Alembic configurado para migrations
- [ ] Migration inicial criada e aplicada
- [ ] Repositórios concretos implementados
- [ ] Testes de integração passando

---

## 📦 FASES 6-9: Continuação

As fases restantes seguem o mesmo padrão:

- **Fase 6:** Integração WhatsApp (Cloud API ou biblioteca)
- **Fase 7:** Handler de mensagens conectando tudo
- **Fase 8:** Testes completos (unit, integration, e2e)
- **Fase 9:** Docker e deploy

---

## 📚 Recursos para Estudo

### Documentação Oficial

| Recurso | Link |
|---------|------|
| Python 3.12 | https://docs.python.org/3.12/ |
| FastAPI | https://fastapi.tiangolo.com/ |
| SQLAlchemy 2.0 | https://docs.sqlalchemy.org/en/20/ |
| Pydantic | https://docs.pydantic.dev/latest/ |
| pytest | https://docs.pytest.org/ |
| WhatsApp Cloud API | https://developers.facebook.com/docs/whatsapp/cloud-api |
| UV Package Manager | https://docs.astral.sh/uv/ |

### Cursos Recomendados (Gratuitos)

1. **Python** - https://docs.python.org/3/tutorial/
2. **FastAPI** - Documentação oficial é excelente
3. **SQLAlchemy** - Tutorial oficial
4. **Clean Architecture** - Artigos do Uncle Bob

---

## 🆘 Troubleshooting Comum

### Erro: "ModuleNotFoundError"
- Verificar se ambiente virtual está ativado
- Verificar se pacote está instalado: `uv pip list`

### Erro: "Connection refused" (Database)
- Verificar se PostgreSQL está rodando
- Verificar DATABASE_URL no .env

### Erro: "Rate limited" (WhatsApp)
- Reduzir frequência de mensagens
- Implementar queue com delay

---

## 📋 Checklist Geral do Projeto

### Setup
- [ ] Fase 0: Ambiente configurado
- [ ] Fase 1: Estrutura criada

### Domínio
- [ ] Fase 2: Entidades implementadas
- [ ] Fase 3: Interfaces definidas

### Aplicação
- [ ] Fase 4: Casos de uso prontos

### Infraestrutura
- [ ] Fase 5: Banco configurado
- [ ] Fase 6: WhatsApp integrado
- [ ] Fase 7: Handler funcionando

### Qualidade
- [ ] Fase 8: Testes passando

### Deploy
- [ ] Fase 9: Docker configurado

---

## 📝 Notas para IA Assistente

### Ao Iniciar Cada Fase

1. Anunciar qual fase está iniciando
2. Explicar o objetivo da fase
3. Mostrar o que será feito
4. Pedir confirmação para prosseguir

### Ao Completar Cada Fase

1. Mostrar código/arquivos criados
2. Rodar testes automaticamente
3. Mostrar resultado dos testes
4. Listar o que foi concluído
5. PEDIR PERMISSÃO para próxima fase

### Formato de Resposta

```markdown
## 🚀 Iniciando Fase X: [Nome da Fase]

**Objetivo:** [Descrição]

**O que vou fazer:**
1. [Ação 1]
2. [Ação 2]
3. [Ação 3]

**Por que estou fazendo isso:**
[Explicação técnica]

**Fontes consultadas:**
- [Link 1]
- [Link 2]

Posso prosseguir? (sim/não)
```

---

## 🔄 Histórico de Versões

| Versão | Data | Alterações |
|--------|------|------------|
| 1.0.0 | Jan 2026 | Versão inicial - Adaptado para Python |

---

**FIM DO DOCUMENTO DE CONTEXTO**

*Este documento deve ser consultado pela IA assistente antes de cada ação no projeto.*