# 📚 Guia de Estudo - WhatsApp E-commerce Bot

## 📖 Introdução

Este documento foi criado para você estudar e entender **cada passo** do desenvolvimento do projeto. Aqui você vai aprender Python, Git, Clean Architecture e boas práticas de desenvolvimento.

---

# 🚀 FASE 0: Setup do Ambiente e Git

## 🎯 Objetivo da Fase 0

Configurar todo o ambiente de desenvolvimento antes de começar a programar. Esta é a **fundação** do projeto - sem ela, nada funciona!

---

## 📋 Passo 1: Verificar Instalações

### O que fizemos:
```bash
python --version    # Resultado: Python 3.14.0
git --version       # Resultado: git version 2.52.0
uv --version        # Resultado: uv 0.9.28
```

### Por que isso é importante:
- **Python**: É a linguagem que usaremos para programar todo o bot.
- **Git**: É o sistema de controle de versão. Pense nele como um "histórico de alterações" do seu código. Se você errar algo, pode voltar atrás!
- **UV**: É um gerenciador de pacotes moderno para Python (mais rápido que pip).

### Conceitos Aprendidos:

#### O que é Python?
Python é uma linguagem de programação de alto nível, conhecida por sua sintaxe limpa e fácil de aprender. É muito usada para:
- Desenvolvimento web (Django, FastAPI, Flask)
- Automação e scripts
- Análise de dados e IA
- Bots e automações

#### O que é Git?
Git é um **sistema de controle de versão distribuído**. Isso significa que:
1. Ele salva o histórico de todas as mudanças no código
2. Permite trabalhar em equipe sem conflitos
3. Você pode criar "branches" (ramificações) para testar coisas novas
4. Se algo der errado, você pode voltar para uma versão anterior

#### O que é UV?
UV é um gerenciador de pacotes para Python, criado em Rust. Ele é:
- **10-100x mais rápido** que pip
- Gerencia ambientes virtuais automaticamente
- Resolve dependências de forma mais inteligente

---

## 📋 Passo 2: Inicializar o Repositório Git

### Comando executado:
```bash
git init
```

### O que aconteceu:
Foi criada uma pasta oculta chamada `.git/` que contém todo o histórico do projeto.

### Estrutura criada:
```
📁 WhatsApp chatBot/
└── 📁 .git/           # ← Pasta do Git (oculta)
    ├── HEAD           # Indica qual branch está ativa
    ├── config         # Configurações do repositório
    ├── objects/       # Aqui ficam os arquivos versionados
    └── refs/          # Referências para branches e tags
```

### Conceitos Aprendidos:

#### Repositório Git
Um repositório é uma pasta que está sendo "vigiada" pelo Git. Toda mudança em arquivos dentro dessa pasta pode ser rastreada.

#### Commit
Pense em um commit como uma "foto" do seu código em um momento específico. Cada commit tem:
- Um **ID único** (hash) - ex: `76cea64`
- Uma **mensagem** descrevendo o que foi feito
- A **data/hora** do commit
- O **autor** do commit

---

## 📋 Passo 3: Criar o arquivo .gitignore

### O que é .gitignore?
É um arquivo que diz ao Git quais arquivos/pastas ele deve **IGNORAR** (não versionar).

### Por que ignorar arquivos?

1. **Segurança**: Arquivos `.env` contêm senhas e tokens. Se você versionar isso e enviar para o GitHub, qualquer pessoa pode ver suas credenciais!

2. **Limpeza**: Arquivos como `__pycache__/` são gerados automaticamente pelo Python e não precisam estar no repositório.

3. **Tamanho**: Pastas como `.venv/` e `node_modules/` podem ter centenas de MB. Não faz sentido guardar no Git.

### Conteúdo do nosso .gitignore (explicado):

```gitignore
# ===========================================================
# PYTHON - Arquivos gerados pelo interpretador
# ===========================================================
# Quando você roda um arquivo .py, o Python cria uma versão
# "compilada" dele em bytecode (.pyc) para rodar mais rápido.
# Esses arquivos são gerados automaticamente e não devem ser versionados.
__pycache__/          # Pasta com arquivos .pyc
*.py[cod]             # Qualquer arquivo .pyc, .pyo ou .pyd
*$py.class            # Arquivos de classe Java (Jython)

# ===========================================================
# AMBIENTES VIRTUAIS
# ===========================================================
# O ambiente virtual é uma "caixa isolada" com as bibliotecas
# do projeto. Cada desenvolvedor cria o seu próprio.
.venv/                # Nome padrão do ambiente virtual
venv/                 # Nome alternativo
ENV/                  # Outro nome alternativo

# ===========================================================
# VARIÁVEIS DE AMBIENTE - NUNCA VERSIONAR!
# ===========================================================
# ⚠️ ATENÇÃO: Estes arquivos contêm SENHAS e CHAVES SECRETAS!
# Se você versionar e publicar no GitHub, hackers podem:
# - Acessar seu banco de dados
# - Usar sua conta de WhatsApp
# - Gastar seu dinheiro em APIs pagas
.env                  # Arquivo principal de variáveis
.env.local            # Variáveis locais
.env.*.local          # Variáveis por ambiente

# ===========================================================
# IDEs e EDITORES
# ===========================================================
# Cada desenvolvedor pode usar um editor diferente.
# As configurações são pessoais.
.idea/                # PyCharm / IntelliJ
.vscode/              # VS Code
*.swp                 # Vim

# ===========================================================
# WHATSAPP - MUITO SENSÍVEL!
# ===========================================================
# ⚠️ ATENÇÃO: Esses arquivos contêm sua sessão logada!
# Se alguém tiver acesso, pode usar sua conta do WhatsApp!
auth_info/            # Sessão do Baileys
session/              # Sessão genérica
```

### Conceitos Aprendidos:

#### Padrões Glob
No .gitignore usamos padrões "glob" para ignorar múltiplos arquivos:
- `*` = qualquer coisa (ex: `*.log` ignora todos os arquivos .log)
- `**` = qualquer pasta (ex: `**/__pycache__` ignora em qualquer subpasta)
- `?` = um caractere qualquer
- `[abc]` = a, b ou c

---

## 📋 Passo 4: Criar arquivo .python-version

### Comando executado:
Criamos um arquivo `.python-version` contendo apenas:
```
3.14
```

### Para que serve:
Ferramentas como `pyenv` e `uv` leem este arquivo para saber qual versão do Python usar no projeto.

### Benefício:
Quando outro desenvolvedor clonar o projeto, ele saberá exatamente qual versão do Python usar. Isso evita o famoso problema: "Na minha máquina funciona!"

---

## 📋 Passo 5: Inicializar Projeto com UV

### Comando executado:
```bash
python -m uv init --name whatsapp-ecommerce-bot
```

### O que aconteceu:
O UV criou automaticamente os arquivos:
- `pyproject.toml` - Configuração do projeto
- `main.py` - Arquivo principal (Hello World)
- `README.md` - Documentação (vazio)

### O que é pyproject.toml?

É o arquivo de configuração padrão para projetos Python modernos. Ele substitui os antigos `setup.py` e `requirements.txt`.

```toml
[project]
name = "whatsapp-ecommerce-bot"   # Nome do projeto
version = "0.1.0"                  # Versão atual
description = "Add your description here"
readme = "README.md"               # Arquivo de documentação
requires-python = ">=3.14"         # Versão mínima do Python
dependencies = []                  # Bibliotecas necessárias (vazio por enquanto)
```

### Conceitos Aprendidos:

#### Versionamento Semântico (SemVer)
A versão `0.1.0` segue o padrão semântico:
- **MAJOR.MINOR.PATCH** = 0.1.0
- **MAJOR** (0): Mudanças incompatíveis (breaking changes)
- **MINOR** (1): Novas funcionalidades compatíveis
- **PATCH** (0): Correções de bugs

Versões começando com 0.x.x indicam que o software ainda está em desenvolvimento inicial.

---

## 📋 Passo 6: Criar Ambiente Virtual

### Comando executado:
```bash
python -m uv venv
```

### O que é um Ambiente Virtual?

Imagine que você tem dois projetos:
- Projeto A usa `requests==2.28`
- Projeto B usa `requests==2.31`

Sem ambiente virtual, você teria conflito! Com ambiente virtual, cada projeto tem sua própria "caixa" isolada de bibliotecas.

### Estrutura criada:
```
📁 .venv/                    # Ambiente virtual
├── 📁 Lib/                  # Bibliotecas instaladas
│   └── 📁 site-packages/    # Seus pacotes Python ficam aqui
├── 📁 Scripts/              # Executáveis (Windows)
│   ├── python.exe           # Python isolado
│   ├── pip.exe              # Pip isolado
│   └── activate             # Script para ativar o ambiente
└── pyvenv.cfg               # Configuração do ambiente
```

### Como ativar o ambiente virtual:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### Como saber se está ativado:
Quando ativado, você verá `(.venv)` antes do prompt:
```
(.venv) PS C:\Users\User\Desktop\WhatsApp chatBot>
```

---

## 📋 Passo 7: Configurar Identidade Git

### Comandos executados:
```bash
git config user.email "user@example.com"
git config user.name "Developer"
```

### Por que isso é necessário:
O Git precisa saber **quem** está fazendo cada commit. Isso é importante para:
1. Identificar quem fez cada mudança
2. Contato em caso de dúvidas sobre o código
3. Histórico de responsabilidades

### Diferença entre --global e sem flag:
```bash
git config --global user.email "email"  # Configura para TODOS os projetos
git config user.email "email"           # Configura só para ESTE projeto
```

---

## 📋 Passo 8: Primeiro Commit

### Comandos executados:
```bash
git add .                                              # Adiciona todos os arquivos
git commit -m "chore: setup inicial do projeto - Fase 0 completa"
```

### O que cada comando faz:

#### `git add .`
Adiciona arquivos à **staging area** (área de preparação). Pense assim:
1. Você modifica arquivos (working directory)
2. Você escolhe quais adicionar ao próximo commit (`git add`)
3. Você cria o commit (`git commit`)

```
┌─────────────────┐    git add     ┌──────────────┐    git commit    ┌────────────┐
│ Working         │ ─────────────> │ Staging Area │ ────────────────>│ Repository │
│ Directory       │                │ (Index)      │                  │ (.git)     │
└─────────────────┘                └──────────────┘                  └────────────┘
   Arquivos                        Arquivos prontos                   Histórico
   modificados                     para commit                        permanente
```

#### `git commit -m "mensagem"`
Cria um commit com a mensagem especificada.

### Padrão de Mensagens de Commit (Conventional Commits)

Usamos o padrão **Conventional Commits** para mensagens claras:

```
tipo(escopo): descrição curta
```

**Tipos comuns:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Formatação (não afeta lógica)
- `refactor`: Refatoração de código
- `test`: Adição/modificação de testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```
feat(auth): adicionar login com Google
fix(cart): corrigir cálculo de frete
docs(readme): atualizar instruções de instalação
chore: atualizar dependências
```

### Resultado do nosso commit:
```
[master (root-commit) 76cea64] chore: setup inicial do projeto - Fase 0 completa
 6 files changed, 2510 insertions(+)
```

Isso significa:
- `76cea64` - ID único do commit (hash)
- `root-commit` - É o primeiro commit do repositório
- `6 files changed` - 6 arquivos foram adicionados
- `2510 insertions(+)` - 2510 linhas foram adicionadas

---

## 📋 Passo 9: Verificação Final

### Comandos de verificação:

```bash
# Ver status do repositório
git status
# Resultado: "On branch master, nothing to commit"

# Ver histórico de commits
git log --oneline
# Resultado: "76cea64 chore: setup inicial do projeto - Fase 0 completa"

# Testar se o projeto funciona
.venv\Scripts\python.exe main.py
# Resultado: "Hello from whatsapp-ecommerce-bot!"
```

---

## ✅ Checklist da Fase 0

Verifique se você entendeu tudo:

- [x] **Git inicializado** - Comando `git init` cria a pasta `.git/`
- [x] **.gitignore configurado** - Lista de arquivos que o Git deve ignorar
- [x] **pyproject.toml criado** - Configuração do projeto Python moderno
- [x] **Ambiente virtual criado** - Pasta `.venv/` isola as dependências
- [x] **Primeiro commit feito** - Snapshot inicial do projeto

---

## 📁 Estrutura Final da Fase 0

```
📁 WhatsApp chatBot/
├── 📁 .git/                 # Repositório Git (oculto)
├── 📁 .venv/                # Ambiente Virtual Python (oculto)
│   ├── 📁 Lib/              # Bibliotecas instaladas
│   └── 📁 Scripts/          # python.exe, pip.exe, activate
├── 📄 .gitignore            # Arquivos ignorados pelo Git
├── 📄 .python-version       # Versão do Python: 3.14
├── 📄 README.md             # Documentação do projeto
├── 📄 claude.md             # Especificação técnica detalhada
├── 📄 main.py               # Arquivo principal (Hello World)
└── 📄 pyproject.toml        # Configuração do projeto
```

---

## 🔗 Comandos Úteis (Referência Rápida)

### Git
```bash
git status              # Ver estado atual
git add .               # Adicionar tudo ao staging
git commit -m "msg"     # Criar commit
git log --oneline       # Ver histórico resumido
git diff                # Ver diferenças não commitadas
```

### Ambiente Virtual
```bash
python -m uv venv       # Criar ambiente virtual
.venv\Scripts\Activate  # Ativar (Windows PowerShell)
deactivate              # Desativar
```

### Python
```bash
python --version        # Ver versão
python arquivo.py       # Executar script
python -m pip list      # Listar pacotes instalados
```

---

## 📚 Para Estudar Mais

1. **Git**: https://git-scm.com/book/pt-br/v2 (Livro oficial em PT-BR)
2. **Python**: https://docs.python.org/pt-br/3/tutorial/ (Tutorial oficial)
3. **UV**: https://docs.astral.sh/uv/ (Documentação oficial)
4. **Conventional Commits**: https://www.conventionalcommits.org/pt-br/

---

## ➡️ Próxima Fase

Na **Fase 1** vamos:
1. Criar toda a estrutura de pastas (Clean Architecture)
2. Instalar todas as dependências (FastAPI, SQLAlchemy, etc.)
3. Criar o sistema de configurações
4. Preparar o projeto para receber código de verdade!

---

*Documento criado em: Janeiro 2026*
*Projeto: WhatsApp E-commerce Bot*

---

# 🚀 FASE 1: Estrutura Base e Configurações

## 🎯 Objetivo da Fase 1

Criar a estrutura de pastas seguindo a **Clean Architecture** e configurar todas as dependências do projeto.

---

## 📋 Passo 1: Entendendo a Clean Architecture

### O que é Clean Architecture?

Clean Architecture é uma forma de organizar código criada por **Robert C. Martin** (Uncle Bob). A ideia principal é:

> **Separar o código em camadas que não dependem de detalhes externos.**

```
┌───────────────────────────────────────────────────┐
│                  PRESENTATION                      │
│        (API REST, Handlers do WhatsApp)           │
└─────────────────────┬─────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────┐
│                  APPLICATION                       │
│              (Casos de Uso)                        │
└─────────────────────┬─────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────┐
│                    DOMAIN                          │
│         (Entidades, Regras de Negócio)            │
└───────────────────────────────────────────────────┘
                      ▲
                      │
┌───────────────────────────────────────────────────┐
│                 INFRASTRUCTURE                     │
│         (Banco de Dados, APIs Externas)           │
└───────────────────────────────────────────────────┘
```

### Por que usar Clean Architecture?

1. **Testabilidade**: Fácil testar cada camada isoladamente
2. **Manutenibilidade**: Mudanças em uma camada não afetam outras
3. **Independência de Frameworks**: O domínio não sabe que existe FastAPI
4. **Independência de Banco**: O domínio não sabe que existe PostgreSQL

### As 4 Camadas do Nosso Projeto

| Camada | Pasta | Responsabilidade |
|--------|-------|-----------------|
| **Domain** | `src/domain/` | Regras de negócio, entidades |
| **Application** | `src/application/` | Casos de uso, orquestração |
| **Infrastructure** | `src/infrastructure/` | Banco, cache, WhatsApp |
| **Presentation** | `src/presentation/` | API REST, webhooks |

---

## 📋 Passo 2: Criando a Estrutura de Pastas

### Comandos usados (Windows PowerShell):

```powershell
# Criar pastas do src
New-Item -ItemType Directory -Force -Path `
    "src/domain/entities", `
    "src/domain/repositories", `
    "src/domain/services", `
    "src/application/usecases", `
    "src/application/dtos", `
    "src/infrastructure/database/repositories", `
    "src/infrastructure/cache", `
    "src/infrastructure/whatsapp", `
    "src/presentation/api/routes", `
    "src/presentation/whatsapp", `
    "src/config", `
    "src/shared/errors", `
    "src/shared/utils", `
    "src/shared/types"

# Criar pastas de testes
New-Item -ItemType Directory -Force -Path `
    "tests/unit/domain/entities", `
    "tests/unit/application", `
    "tests/unit/infrastructure", `
    "tests/integration", `
    "tests/e2e"
```

### Estrutura Final:

```
📁 src/
├── 📁 domain/           # Camada mais interna (regras de negócio)
│   ├── 📁 entities/     # Objetos do negócio (Customer, Product)
│   ├── 📁 repositories/ # Interfaces de acesso a dados
│   └── 📁 services/     # Serviços de domínio
│
├── 📁 application/      # Camada de aplicação
│   ├── 📁 usecases/     # Casos de uso (HandleMessage, GetProducts)
│   └── 📁 dtos/         # Objetos de transferência de dados
│
├── 📁 infrastructure/   # Camada de infraestrutura
│   ├── 📁 database/     # SQLAlchemy, PostgreSQL
│   ├── 📁 cache/        # Redis
│   └── 📁 whatsapp/     # Cliente WhatsApp
│
├── 📁 presentation/     # Camada de apresentação
│   ├── 📁 api/          # FastAPI REST
│   └── 📁 whatsapp/     # Handlers de mensagens
│
├── 📁 config/           # Configurações (settings.py)
└── 📁 shared/           # Código compartilhado
    ├── 📁 errors/       # Exceções customizadas
    ├── 📁 utils/        # Funções utilitárias
    └── 📁 types/        # Enums e tipos globais
```

---

## 📋 Passo 3: Arquivos __init__.py

### O que é __init__.py?

Em Python, uma pasta só é reconhecida como **pacote** (módulo importável) se tiver um arquivo `__init__.py`.

```python
# Sem __init__.py:
from src.domain.entities import Customer  # ❌ ERRO: não é um pacote

# Com __init__.py:
from src.domain.entities import Customer  # ✅ Funciona!
```

### Conteúdo dos nossos __init__.py:

Cada arquivo tem uma **docstring** explicando o propósito da pasta:

```python
# src/domain/__init__.py
"""
Camada de DOMÍNIO (Domain Layer).

Esta é a camada mais interna da Clean Architecture.
REGRAS:
- Esta camada NÃO depende de nenhuma outra
- NÃO importar nada de infrastructure ou presentation
"""
```

---

## 📋 Passo 4: Configurando pyproject.toml

### O que é pyproject.toml?

É o arquivo de configuração padrão para projetos Python modernos. Ele substitui:
- `setup.py` (configuração do pacote)
- `requirements.txt` (dependências)
- `setup.cfg` (configurações extras)

### Estrutura do pyproject.toml:

```toml
# [project] - Metadados do projeto
[project]
name = "whatsapp-ecommerce-bot"
version = "0.1.0"
requires-python = ">=3.12"

# dependencies - Bibliotecas que o projeto PRECISA
dependencies = [
    "fastapi>=0.109.0",      # Web Framework
    "pydantic>=2.5.0",       # Validação
    "sqlalchemy>=2.0.25",    # ORM
    "redis>=5.0.0",          # Cache
]

# [project.optional-dependencies] - Só para desenvolvimento
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",         # Testes
    "ruff>=0.1.0",           # Linter
    "mypy>=1.8.0",           # Type checking
]
```

### Nossas Dependências Explicadas:

| Biblioteca | Propósito | Documentação |
|------------|-----------|--------------|
| **fastapi** | API REST moderna e rápida | https://fastapi.tiangolo.com/ |
| **pydantic** | Validação de dados | https://docs.pydantic.dev/ |
| **sqlalchemy** | ORM para banco de dados | https://docs.sqlalchemy.org/ |
| **redis** | Cache e sessões | https://redis.io/docs/ |
| **httpx** | Cliente HTTP assíncrono | https://www.python-httpx.org/ |
| **structlog** | Logging estruturado | https://www.structlog.org/ |

---

## 📋 Passo 5: Variáveis de Ambiente (.env)

### O que são variáveis de ambiente?

São valores de configuração que ficam **fora do código**. Isso é importante porque:

1. **Segurança**: Senhas não ficam no código (que pode ir pro GitHub)
2. **Flexibilidade**: Mudar configurações sem alterar código
3. **Ambientes**: Valores diferentes para dev/staging/produção

### Arquivo .env.example (template):

```env
# App
APP_NAME=whatsapp-ecommerce-bot
APP_ENV=development       # development, staging, production
DEBUG=true

# NUNCA compartilhe este valor!
SECRET_KEY=sua-chave-secreta-aqui

# Banco de Dados
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db

# Cache
REDIS_URL=redis://localhost:6379/0
```

### Fluxo de uso:

```
1. Copiar template:  cp .env.example .env
2. Editar valores:   (preencher senhas reais)
3. .env está no .gitignore (não vai pro Git)
```

---

## 📋 Passo 6: Pydantic Settings

### O que é Pydantic Settings?

Uma biblioteca que carrega variáveis de ambiente e as valida automaticamente.

### Como funciona:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Cada atributo = uma variável de ambiente
    app_name: str = "default"      # APP_NAME no .env
    debug: bool = False            # DEBUG no .env
    secret_key: str                # SECRET_KEY (obrigatório!)
    
# A mágica acontece aqui:
settings = Settings()  # Carrega .env automaticamente!
print(settings.app_name)  # "whatsapp-ecommerce-bot"
```

### Benefícios:

1. **Validação de tipos**: Se `DEBUG=abc`, dá erro (esperava bool)
2. **Valores obrigatórios**: Se `SECRET_KEY` não existir, erro
3. **Valores padrão**: Se `APP_NAME` não existir, usa "default"
4. **Documentação automática**: Type hints servem como docs

### O decorator @lru_cache:

```python
from functools import lru_cache

@lru_cache  # Cacheia o resultado
def get_settings() -> Settings:
    return Settings()

# Primeira chamada: cria Settings (lê .env)
get_settings()

# Segunda chamada: retorna o mesmo objeto (não lê .env de novo)
get_settings()
```

---

## 📋 Passo 7: Instalando Dependências

### Comando usado:

```bash
# Ativar ambiente virtual primeiro!
.venv\Scripts\Activate

# Instalar projeto em modo editável + dependências dev
pip install -e ".[dev]"
```

### O que significa `-e ".[dev]"`?

- `-e`: Modo **editável** (edits são refletidos imediatamente)
- `.`: Instala o pacote do diretório atual
- `[dev]`: Inclui as dependências opcionais de desenvolvimento

---

## ✅ Verificação da Fase 1

### Comandos de teste:

```bash
# Testar se settings carrega
python -c "from src.config.settings import get_settings; print(get_settings().app_name)"
# Resultado: whatsapp-ecommerce-bot

# Testar se FastAPI está instalado
python -c "import fastapi; print(fastapi.__version__)"
# Resultado: 0.128.0

# Testar se pytest funciona
pytest --version
# Resultado: pytest 9.0.2
```

---

## ✅ Checklist da Fase 1

- [x] Estrutura de pastas criada (Clean Architecture)
- [x] 22 arquivos `__init__.py` criados
- [x] `pyproject.toml` com todas as dependências
- [x] `.env.example` (template documentado)
- [x] `.env` (arquivo local, não versionado)
- [x] `src/config/settings.py` (Pydantic Settings)
- [x] Dependências instaladas
- [x] Importações funcionando
- [x] Commit da Fase 1 feito

---

## ➡️ Próxima Fase

Na **Fase 2** vamos:
1. Criar as **Entidades de Domínio** (Customer, Product, Order, Session)
2. Criar os **Enums** (OrderStatus, SessionState)
3. Escrever **testes unitários** para as entidades
4. Aprender sobre **dataclasses** do Python

---

*Documento atualizado em: Janeiro 2026*
*Fase 1 concluída com sucesso!*
