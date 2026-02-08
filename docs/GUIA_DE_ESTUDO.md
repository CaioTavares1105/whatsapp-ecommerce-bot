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

---

# 🚀 FASE 2: Camada de Domínio (Entidades)

## 🎯 Objetivo da Fase 2

Criar as **entidades de domínio** do sistema - os objetos principais que representam o negócio.

---

## 📋 Passo 1: O que são Entidades de Domínio?

### Conceito

Entidades são objetos com **IDENTIDADE própria** que persistem ao longo do tempo.

Exemplo: Um **Customer** continua sendo o mesmo cliente mesmo se mudar de nome ou email. A identidade dele (ID) permanece.

### Diferença entre Entidade e Value Object

| Tipo | Identificação | Exemplo |
|------|---------------|---------|
| **Entidade** | Por ID único | Customer, Product, Order |
| **Value Object** | Por atributos | Endereço, Dinheiro, Email |

```python
# Entidade: igualdade por ID
customer1 = Customer(id="123", name="João")
customer2 = Customer(id="123", name="Maria")
# customer1 e customer2 são "o mesmo cliente" (mesmo ID)

# Value Object: igualdade por valor
endereco1 = Endereco(rua="A", numero=10)
endereco2 = Endereco(rua="A", numero=10)
# endereco1 == endereco2 (mesmo conteúdo)
```

---

## 📋 Passo 2: Dataclasses do Python

### O que é @dataclass?

É um **decorator** que gera automaticamente métodos como `__init__`, `__repr__`, `__eq__`.

### Sem dataclass (muito código):
```python
class Customer:
    def __init__(self, phone, name):
        self.phone = phone
        self.name = name
    
    def __repr__(self):
        return f"Customer(phone={self.phone}, name={self.name})"
    
    def __eq__(self, other):
        return self.phone == other.phone and self.name == other.name
```

### Com dataclass (muito mais simples):
```python
from dataclasses import dataclass

@dataclass
class Customer:
    phone: str
    name: str
# __init__, __repr__ e __eq__ são gerados automaticamente!
```

### Recursos importantes do dataclass:

```python
from dataclasses import dataclass, field
import uuid

@dataclass
class Customer:
    # Atributos obrigatórios (sem valor padrão)
    phone_number: str
    
    # Atributos opcionais (com valor padrão)
    name: str | None = None  # str OU None
    
    # Atributos gerados automaticamente
    # field(default_factory=...) cria valor DIFERENTE para cada instância
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
```

### O método __post_init__:

Chamado **APÓS** o `__init__` gerado pelo @dataclass. Usado para validações:

```python
@dataclass
class Customer:
    phone_number: str
    
    def __post_init__(self):
        # Valida telefone após receber os dados
        if len(self.phone_number) < 10:
            raise ValueError("Telefone inválido!")
```

---

## 📋 Passo 3: Enums (Enumerações)

### O que são Enums?

Conjuntos **fixos** de valores possíveis. Evitam "magic strings" soltas no código.

### Sem enum (ruim):
```python
order.status = "pending"  # E se digitar "pendinng"? Erro silencioso!
```

### Com enum (bom):
```python
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"

order.status = OrderStatus.PENDING  # Autocompletar no IDE!
```

### Por que herdar de str?
```python
# Herdar de str permite comparar diretamente:
OrderStatus.PENDING == "pending"  # True!
```

### Nossos enums:

| Enum | Valores | Uso |
|------|---------|-----|
| **OrderStatus** | PENDING, CONFIRMED, PROCESSING, SHIPPED, DELIVERED, CANCELLED | Ciclo de vida do pedido |
| **SessionState** | INITIAL, MENU, PRODUCTS, ORDER_STATUS, FAQ, HUMAN_TRANSFER | Estado do chat |
| **MessageDirection** | INCOMING, OUTGOING | Direção da mensagem |

---

## 📋 Passo 4: Nossas 4 Entidades

### 1. Customer (Cliente)
```python
@dataclass
class Customer:
    phone_number: str          # Telefone WhatsApp (obrigatório)
    name: str | None = None    # Nome (opcional)
    email: str | None = None   # Email (opcional)
    id: str = field(...)       # UUID gerado automaticamente
    
    def update_name(self, name: str) -> None: ...
    def update_email(self, email: str) -> None: ...
```

### 2. Product (Produto)
```python
@dataclass
class Product:
    name: str                  # Nome do produto
    price: Decimal             # Preço (usar Decimal!)
    category: str              # Categoria
    stock: int = 0             # Quantidade em estoque
    active: bool = True        # Se está à venda
    
    @property
    def is_available(self) -> bool:
        return self.active and self.stock > 0
    
    def decrease_stock(self, quantity: int) -> None: ...
```

### 3. Order (Pedido)
```python
@dataclass
class Order:
    customer_id: str           # ID do cliente
    total: Decimal             # Valor total
    status: OrderStatus = OrderStatus.PENDING
    
    def confirm(self) -> None: ...   # PENDING -> CONFIRMED
    def cancel(self) -> None: ...    # -> CANCELLED (se permitido)
    def ship(self) -> None: ...      # PROCESSING -> SHIPPED
```

### 4. Session (Sessão de Chat)
```python
@dataclass  
class Session:
    customer_id: str           # ID do cliente
    state: SessionState = SessionState.INITIAL
    context: dict = field(default_factory=dict)  # Dados temporários
    expires_at: datetime = ...  # Expira em 24h
    
    def update_state(self, new_state: SessionState) -> None: ...
    def set_context(self, key: str, value: Any) -> None: ...
    def get_context(self, key: str, default: Any = None) -> Any: ...
```

---

## 📋 Passo 5: Testes Unitários com Pytest

### O que são Testes Unitários?

Testes que verificam uma **unidade isolada** de código (função, classe, método).

### Por que testar?

1. **Confiança**: Saber que o código funciona
2. **Documentação**: Testes mostram como usar o código
3. **Refatoração**: Alterar código sem medo de quebrar
4. **Debugging**: Encontrar bugs antes da produção

### Framework: Pytest

O framework de testes mais popular do Python. Vantagens:
- Sintaxe simples (`assert`)
- Descoberta automática de testes
- Fixtures para setup/teardown
- Plugins (cobertura, async, etc.)

### Estrutura de um Teste (AAA):

```python
def test_create_customer():
    # ARRANGE (Preparar)
    phone = "5511999999999"
    name = "João"
    
    # ACT (Agir)
    customer = Customer(phone_number=phone, name=name)
    
    # ASSERT (Verificar)
    assert customer.phone_number == phone
    assert customer.name == name
```

### Testando Erros (exceptions):

```python
import pytest

def test_invalid_phone_raises_error():
    with pytest.raises(ValueError) as exc_info:
        Customer(phone_number="123")  # Muito curto!
    
    # Verifica a mensagem do erro
    assert "inválido" in str(exc_info.value).lower()
```

### Convenções de Nomenclatura:

| Tipo | Padrão |
|------|--------|
| Arquivo | `test_*.py` ou `*_test.py` |
| Classe | `Test*` (ex: `TestCustomer`) |
| Método | `test_*` (ex: `test_create_customer`) |

### Como Rodar os Testes:

```bash
# Rodar todos os testes
pytest

# Modo verbose (detalhado)
pytest -v

# Só testes de uma pasta
pytest tests/unit/domain/entities/

# Com cobertura de código
pytest --cov=src

# Só testes que contenham "customer" no nome
pytest -k "customer"
```

---

## 📋 Passo 6: Nossos Testes

### Arquivos criados:
- `tests/unit/domain/entities/test_customer.py`
- `tests/unit/domain/entities/test_product.py`
- `tests/unit/domain/entities/test_order.py`
- `tests/unit/domain/entities/test_session.py`

### Resultado:
```
collected 52 items
...
52 passed in 1.5s
Coverage: 85%
```

### Exemplo de teste completo:

```python
class TestCustomer:
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
        customer = Customer(phone_number="+55 (11) 99999-9999")
        assert customer.phone_number == "5511999999999"
    
    def test_invalid_phone_raises_error(self):
        """Deve erro com telefone inválido."""
        with pytest.raises(ValueError):
            Customer(phone_number="123")
```

---

## ✅ Checklist da Fase 2

- [x] Criar `enums.py` (OrderStatus, SessionState, MessageDirection)
- [x] Criar `customer.py` com validações
- [x] Criar `product.py` com controle de estoque
- [x] Criar `order.py` com máquina de estados
- [x] Criar `session.py` com contexto e expiração
- [x] Criar 4 arquivos de testes unitários
- [x] 52 testes passando
- [x] Cobertura de 85%
- [x] Commit da Fase 2 feito

---

## 📚 Conceitos Python Aprendidos

| Conceito | Descrição |
|----------|-----------|
| `@dataclass` | Gera `__init__`, `__repr__`, `__eq__` automaticamente |
| `field(default_factory=...)` | Gera valor diferente para cada instância |
| `__post_init__` | Chamado após `__init__` para validações |
| `@property` | Transforma método em atributo (sem parênteses) |
| `Decimal` | Precisão exata para valores monetários |
| `Enum` | Conjunto fixo de valores possíveis |
| `str \| None` | Tipo que pode ser string OU None |
| `pytest.raises()` | Testa se uma exceção é levantada |

---

*Documento atualizado em: Fevereiro 2026*
*Fase 2 concluída com sucesso!*

---

# 🚀 FASE 3: Interfaces de Repositório

## 🎯 Objetivo da Fase 3

Criar **interfaces (contratos)** para acesso a dados usando Abstract Base Classes (ABC).

---

## 📋 Passo 1: O que é o Padrão Repository?

### Conceito

O **Repository Pattern** é um padrão de design que:
- Isola a lógica de acesso a dados
- Permite trocar tecnologia (PostgreSQL → MongoDB) sem mudar o domínio
- Facilita testes com "mocks"

### Diagrama

```
┌─────────────────┐      ┌──────────────────────┐      ┌─────────────┐
│   Use Case      │ ───► │   ICustomerRepository │ ◄─── │   Domínio   │
│   (Aplicação)   │      │   (Interface/ABC)    │      │   (Regras)  │
└─────────────────┘      └───────────┬──────────┘      └─────────────┘
                                     │
                                     │ "implementa"
                                     ▼
                    ┌────────────────────────────────┐
                    │   PostgresCustomerRepository    │
                    │   (Implementação Concreta)      │
                    │   Usa SQLAlchemy                │
                    └────────────────────────────────┘
```

### Analogia

Pense numa **tomada elétrica**:
- A **interface** é o formato da tomada (2 ou 3 pinos)
- A **implementação** é o aparelho conectado
- Qualquer aparelho que siga o "contrato" funciona!

---

## 📋 Passo 2: Abstract Base Class (ABC)

### O que é ABC?

ABC é a forma do Python de criar **interfaces** e **classes abstratas**.

```python
from abc import ABC, abstractmethod

class IMinhaInterface(ABC):
    
    @abstractmethod
    def metodo_obrigatorio(self):
        """Subclasses DEVEM implementar."""
        ...
```

### Regras importantes:

1. **Herdar de ABC**: A classe deve herdar de `abc.ABC`
2. **@abstractmethod**: Marca métodos que DEVEM ser implementados
3. **Não pode instanciar**: `IMinhaInterface()` dá erro!
4. **Subclasse deve implementar**: Se não implementar, dá erro

### Exemplo prático:

```python
# Interface (contrato)
class IAnimal(ABC):
    @abstractmethod
    def fazer_som(self) -> str:
        ...

# Implementação 1
class Cachorro(IAnimal):
    def fazer_som(self) -> str:
        return "Au au!"

# Implementação 2
class Gato(IAnimal):
    def fazer_som(self) -> str:
        return "Miau!"

# ERRO! Não implementou fazer_som
class AnimalIncompleto(IAnimal):
    pass

AnimalIncompleto()  # TypeError!
```

---

## 📋 Passo 3: Por que usar async/await?

### O problema

Acesso a banco de dados é **lento** (I/O bound):
- Envia query para o banco
- Espera resposta (pode demorar 10-100ms)
- Recebe resultado

### Sem async (bloqueante):

```python
# Thread fica PARADA esperando banco
resultado = banco.execute("SELECT * FROM users")  # Bloqueia!
# Nenhum outro request é processado nesse tempo
```

### Com async (não-bloqueante):

```python
# Thread LIBERA enquanto espera banco
resultado = await banco.execute("SELECT * FROM users")
# Outros requests podem ser processados!
```

### Conclusão

Por isso, todos os métodos dos repositórios são `async`:

```python
@abstractmethod
async def find_by_id(self, id: str) -> Customer | None:
    ...
```

---

## 📋 Passo 4: Nossas 4 Interfaces

### 1. ICustomerRepository

```python
class ICustomerRepository(ABC):
    async def find_by_phone(self, phone: str) -> Customer | None: ...
    async def find_by_id(self, id: str) -> Customer | None: ...
    async def find_all(self) -> list[Customer]: ...
    async def save(self, customer: Customer) -> None: ...
    async def update(self, customer: Customer) -> None: ...
    async def delete(self, id: str) -> None: ...
```

### 2. IProductRepository

```python
class IProductRepository(ABC):
    async def find_by_id(self, id: str) -> Product | None: ...
    async def find_by_category(self, category: str) -> list[Product]: ...
    async def find_all_active(self) -> list[Product]: ...
    async def search(self, query: str) -> list[Product]: ...
    async def list_categories(self) -> list[str]: ...
    async def save(self, product: Product) -> None: ...
    async def update(self, product: Product) -> None: ...
```

### 3. IOrderRepository

```python
class IOrderRepository(ABC):
    async def find_by_id(self, id: str) -> Order | None: ...
    async def find_by_customer(self, customer_id: str) -> list[Order]: ...
    async def find_by_status(self, status: OrderStatus) -> list[Order]: ...
    async def save(self, order: Order) -> None: ...
    async def update(self, order: Order) -> None: ...
    async def count_by_status(self, status: OrderStatus) -> int: ...
```

### 4. ISessionRepository

```python
class ISessionRepository(ABC):
    async def find_by_id(self, id: str) -> Session | None: ...
    async def find_by_customer(self, customer_id: str) -> Session | None: ...
    async def find_active_by_phone(self, phone: str) -> Session | None: ...
    async def save(self, session: Session) -> None: ...
    async def update(self, session: Session) -> None: ...
    async def delete_expired(self) -> int: ...
```

---

## 📋 Passo 5: Como usar as interfaces

### Import centralizado:

```python
from src.domain.repositories import (
    ICustomerRepository,
    IProductRepository,
    IOrderRepository,
    ISessionRepository,
)
```

### Injeção de Dependência:

```python
class ProcessarMensagemUseCase:
    def __init__(
        self,
        customer_repo: ICustomerRepository,  # Interface, não implementação!
        session_repo: ISessionRepository,
    ):
        self.customer_repo = customer_repo
        self.session_repo = session_repo
    
    async def execute(self, phone: str, message: str):
        customer = await self.customer_repo.find_by_phone(phone)
        session = await self.session_repo.find_active_by_phone(phone)
        # ... lógica de negócio
```

### Benefício: Testes fáceis!

```python
# No teste, passamos um Mock em vez do repositório real
class MockCustomerRepository(ICustomerRepository):
    async def find_by_phone(self, phone: str):
        return Customer(phone_number=phone, name="Teste")
    # ... outros métodos

# Teste usa o mock
use_case = ProcessarMensagemUseCase(
    customer_repo=MockCustomerRepository(),
    session_repo=MockSessionRepository(),
)
```

---

## ✅ Verificação da Fase 3

```bash
# Testar importações
python -c "from src.domain.repositories import ICustomerRepository, IProductRepository, IOrderRepository, ISessionRepository; print('OK!')"

# Resultado esperado: OK!
```

---

## ✅ Checklist da Fase 3

- [x] Criar `ICustomerRepository` com métodos CRUD
- [x] Criar `IProductRepository` com busca por categoria
- [x] Criar `IOrderRepository` com busca por status
- [x] Criar `ISessionRepository` com busca por telefone
- [x] Atualizar `__init__.py` com exports
- [x] Testar importações
- [x] Atualizar documento de estudo

---

## 📚 Conceitos Python Aprendidos

| Conceito | Descrição |
|----------|-----------|
| `abc.ABC` | Classe base para criar interfaces |
| `@abstractmethod` | Marca método como obrigatório na subclasse |
| `async def` | Define função assíncrona (não-bloqueante) |
| `await` | Espera resultado de função async |
| `... (Ellipsis)` | Indica corpo vazio (placeholder) |
| `Customer \| None` | Tipo que pode ser Customer OU None |
| `list[Product]` | Lista tipada de Product |

---

*Documento atualizado em: Fevereiro 2026*
*Fase 3 concluída com sucesso!*

---

# 🚀 FASE 4: Casos de Uso (Application Layer)

## 🎯 Objetivo da Fase 4

Implementar a **camada de aplicação** com Casos de Uso (Use Cases) e DTOs.

---

## 📋 Passo 1: O que é a Camada de Aplicação?

### Conceito

A camada de aplicação é a **orquestradora**:
- Recebe requests da camada de apresentação
- Coordena entidades e repositórios
- Aplica regras de negócio
- Retorna respostas formatadas

### Posição na Clean Architecture

```
┌─────────────────────────────────────────┐
│         Presentation (API/WhatsApp)     │  ← Recebe request
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│         Application (Use Cases)         │  ← ORQUESTRA
└────────────────────┬────────────────────┘
                     │
           ┌─────────┴─────────┐
           │                   │
           ▼                   ▼
┌─────────────────┐  ┌─────────────────────┐
│     Domain      │  │   Infrastructure    │
│   (Entities)    │  │  (Repositories)     │
└─────────────────┘  └─────────────────────┘
```

---

## 📋 Passo 2: O que são DTOs?

### Conceito

**DTO = Data Transfer Object**

São objetos simples que transportam dados entre camadas:
- Não têm lógica de negócio
- São validados automaticamente (Pydantic)
- Separam a API das entidades internas

### Por que usar DTOs?

| Sem DTO | Com DTO |
|---------|---------|
| API conhece entidades | API conhece só DTOs |
| Mudança na entidade quebra API | Mudança interna não afeta API |
| Sem validação automática | Validação automática |

### Nossos DTOs

```python
# Mensagem recebida do usuário
class IncomingMessageDTO(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15)
    text: str = Field(..., min_length=1)
    message_id: str | None = None

# Resposta do bot
class MessageResponseDTO(BaseModel):
    text: str
    should_transfer_to_human: bool = False
    metadata: dict | None = None
```

### Pydantic Field:
```python
from pydantic import Field

# ... = campo obrigatório
phone: str = Field(..., min_length=10)

# Valor padrão
active: bool = Field(default=True)

# Documentação
name: str = Field(..., description="Nome do cliente")
```

---

## 📋 Passo 3: O que são Use Cases?

### Conceito

Use Case = Uma ação do sistema com regras de negócio.

Exemplos:
- `HandleMessageUseCase` - Processar mensagem
- `CreateOrderUseCase` - Criar pedido
- `GetProductsUseCase` - Listar produtos

### Estrutura de um Use Case:

```python
class HandleMessageUseCase:
    def __init__(
        self,
        customer_repo: ICustomerRepository,  # Interfaces!
        session_repo: ISessionRepository,
    ):
        self._customer_repo = customer_repo
        self._session_repo = session_repo
    
    async def execute(self, input: IncomingMessageDTO) -> MessageResponseDTO:
        # 1. Buscar dados
        customer = await self._customer_repo.find_by_phone(input.phone_number)
        
        # 2. Aplicar regras
        if customer is None:
            customer = Customer(phone_number=input.phone_number)
            await self._customer_repo.save(customer)
        
        # 3. Retornar resposta
        return MessageResponseDTO(text="Olá!")
```

### Padrão importante:
- `__init__`: Recebe INTERFACES (não implementações)
- `execute`: Método principal (sempre async)
- Métodos `_privados`: Auxiliares

---

## 📋 Passo 4: HandleMessageUseCase

### Fluxo completo:

```
Mensagem WhatsApp
       │
       ▼
┌──────────────────┐
│ 1. Identificar   │ ← find_by_phone
│    Cliente       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 2. Buscar/Criar  │ ← find_by_customer
│    Sessão        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 3. Identificar   │ ← _identify_intent()
│    Intenção      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 4. Processar     │ ← _handle_greeting, _handle_products...
│    Mensagem      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ 5. Atualizar     │ ← session_repo.update
│    Sessão        │
└────────┬─────────┘
         │
         ▼
    MessageResponseDTO
```

### Intenções identificadas:

| Intenção | Palavras-chave |
|----------|---------------|
| greeting | oi, olá, bom dia |
| products | produto, catálogo, comprar |
| order_status | pedido, rastreio |
| faq | dúvida, ajuda |
| human | atendente, pessoa |
| menu | voltar, início |

---

## 📋 Passo 5: Testes com Mocks

### O que são Mocks?

Mocks são objetos "falsos" que simulam comportamento.

### Por que usar Mocks?

| Com banco real | Com Mocks |
|----------------|-----------|
| Lento (I/O) | Rápido (memória) |
| Precisa configurar banco | Não precisa |
| Dados podem mudar | Dados controlados |

### AsyncMock:

```python
from unittest.mock import AsyncMock

# Cria mock de repositório assíncrono
customer_repo = AsyncMock()

# Define o que deve retornar
customer_repo.find_by_phone.return_value = Customer(phone="123")

# Verifica se foi chamado
customer_repo.save.assert_called_once()
```

### Fixtures do pytest:

```python
@pytest.fixture
def mock_repositories():
    """Cria mocks dos repositórios."""
    return {
        "customer_repo": AsyncMock(),
        "session_repo": AsyncMock(),
    }

@pytest.fixture
def use_case(mock_repositories):
    """Cria use case com mocks injetados."""
    return HandleMessageUseCase(**mock_repositories)
```

### Teste assíncrono:

```python
@pytest.mark.asyncio
async def test_greeting_returns_menu(use_case, mock_repositories):
    # Arrange
    mock_repositories["customer_repo"].find_by_phone.return_value = Customer(...)
    input_dto = IncomingMessageDTO(phone="123", text="Olá")
    
    # Act
    result = await use_case.execute(input_dto)
    
    # Assert
    assert "Bem-vindo" in result.text
```

---

## ✅ Verificação da Fase 4

```bash
# Rodar testes da camada de aplicação
pytest tests/unit/application/ -v

# Rodar TODOS os testes
pytest tests/ -v

# Resultado: 66 passed, 86% coverage
```

---

## ✅ Checklist da Fase 4

- [x] Criar `IncomingMessageDTO` com validações Pydantic
- [x] Criar `MessageResponseDTO` para respostas
- [x] Criar `HandleMessageUseCase` principal
- [x] Implementar identificação de intenções
- [x] Implementar handlers para cada intenção
- [x] Criar 14 testes unitários com Mocks
- [x] Todos os 66 testes passando
- [x] Cobertura de 86%

---

## 📚 Conceitos Python Aprendidos

| Conceito | Descrição |
|----------|-----------|
| `BaseModel` | Classe base Pydantic para DTOs |
| `Field(...)` | Campo obrigatório com validações |
| `AsyncMock` | Mock para funções assíncronas |
| `@pytest.fixture` | Prepara dados reutilizáveis para testes |
| `@pytest.mark.asyncio` | Marca teste como assíncrono |
| `return_value` | Define retorno do mock |
| `assert_called_once()` | Verifica se método foi chamado |
| `**kwargs` | Desempacota dicionário como argumentos |

---

*Documento atualizado em: Fevereiro 2026*
*Fase 4 concluída com sucesso!*

---

# 🚀 FASE 5: Infraestrutura - Banco de Dados

## 🎯 Objetivo da Fase 5

Configurar **PostgreSQL** com **SQLAlchemy 2.0** (ORM assíncrono).

---

## 📋 Passo 1: O que é SQLAlchemy?

### Conceito

**SQLAlchemy** é um ORM (Object-Relational Mapping):
- Mapeia classes Python → tabelas SQL
- Mapeia atributos → colunas
- Mapeia instâncias → linhas

### ORM vs SQL Puro

| SQL Puro | Com ORM |
|----------|---------|
| `SELECT * FROM customers` | `session.query(Customer).all()` |
| Concatenação de strings | Type safety |
| Vulnerável a SQL Injection | Seguro por padrão |

### SQLAlchemy 2.0 (Novo Estilo)

```python
# Antes (1.x)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Agora (2.0) - Com type hints!
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
```

---

## 📋 Passo 2: Modelos SQLAlchemy

### Estrutura de um Modelo

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Classe base para todos os modelos."""
    pass

class CustomerModel(Base):
    __tablename__ = "customers"  # Nome da tabela
    
    # Colunas
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
```

### Tipos de Colunas Comuns

| Python | SQLAlchemy | SQL |
|--------|------------|-----|
| `str` | `String(n)` | `VARCHAR(n)` |
| `int` | `Integer` | `INTEGER` |
| `bool` | `Boolean` | `BOOLEAN` |
| `Decimal` | `Numeric(10,2)` | `NUMERIC(10,2)` |
| `datetime` | `DateTime` | `TIMESTAMP` |
| `dict` | `JSON` | `JSONB` |

### Opções de mapped_column

```python
mapped_column(
    String(100),
    primary_key=True,     # É chave primária?
    unique=True,          # Valores únicos?
    index=True,           # Criar índice?
    nullable=True,        # Pode ser NULL?
    default=0,            # Valor padrão
    onupdate=datetime.now # Atualiza automaticamente
)
```

---

## 📋 Passo 3: Relacionamentos

### Um para Muitos (1:N)

```python
class CustomerModel(Base):
    # Um cliente tem muitos pedidos
    orders: Mapped[list["OrderModel"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )

class OrderModel(Base):
    # Cada pedido pertence a um cliente
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["CustomerModel"] = relationship(back_populates="orders")
```

### Diagrama

```
┌─────────────┐           ┌─────────────┐
│  Customer   │ 1 ───── N │    Order    │
└─────────────┘           └─────────────┘
      │                         │
      └── orders: list[Order]   └── customer_id: FK
```

---

## 📋 Passo 4: Conexão Assíncrona

### Engine

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,       # Log SQL (debug)
    pool_size=5,     # Conexões mantidas
    max_overflow=10  # Extras temporárias
)
```

### Session Factory

```python
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

### Dependency Injection (FastAPI)

```python
async def get_db_session():
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

---

## 📋 Passo 5: Repositório Concreto

### Implementando a Interface

```python
class SQLAlchemyCustomerRepository(ICustomerRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def find_by_phone(self, phone: str) -> Customer | None:
        query = select(CustomerModel).where(
            CustomerModel.phone_number == phone
        )
        result = await self._session.execute(query)
        model = result.scalars().first()
        
        if model is None:
            return None
        
        return self._to_entity(model)
    
    async def save(self, customer: Customer) -> None:
        model = self._to_model(customer)
        self._session.add(model)
        await self._session.flush()
```

### Conversão Model ↔ Entity

```python
def _to_entity(self, model: CustomerModel) -> Customer:
    """Model (banco) → Entity (domínio)"""
    return Customer(
        id=model.id,
        phone_number=model.phone_number,
        name=model.name,
    )

def _to_model(self, entity: Customer) -> CustomerModel:
    """Entity (domínio) → Model (banco)"""
    return CustomerModel(
        id=entity.id,
        phone_number=entity.phone_number,
        name=entity.name,
    )
```

---

## ✅ Verificação da Fase 5

```bash
# Testar imports
python -c "from src.infrastructure.database import Base, CustomerModel"

# Rodar testes
pytest tests/unit/infrastructure/ -v

# Resultado: 28 passed
# Total: 94 passed, 84% coverage
```

---

## ✅ Checklist da Fase 5

- [x] Instalar asyncpg (driver async PostgreSQL)
- [x] Criar `models.py` com 4 modelos
- [x] Criar `connection.py` com engine e session factory
- [x] Criar `SQLAlchemyCustomerRepository`
- [x] Criar 28 testes unitários
- [x] 94 testes passando no total
- [x] 84% de cobertura

---

## 📚 Conceitos Aprendidos

| Conceito | Descrição |
|----------|-----------|
| `DeclarativeBase` | Classe base para modelos SQLAlchemy 2.0 |
| `Mapped[tipo]` | Type hint para colunas |
| `mapped_column()` | Configura coluna da tabela |
| `ForeignKey` | Chave estrangeira |
| `relationship()` | Define relacionamento entre modelos |
| `create_async_engine` | Cria engine assíncrona |
| `async_sessionmaker` | Fábrica de sessões async |
| `select()` | Constrói query SELECT |
| `scalars()` | Extrai objetos do resultado |

---

*Documento atualizado em: Fevereiro 2026*
*Fase 5 concluída com sucesso!*

---

# 🚀 FASE 6: Alembic + Integração WhatsApp

## 🎯 Objetivo da Fase 6

1. Configurar **Alembic** para migrations de banco
2. Criar **WhatsApp Client** para enviar mensagens
3. Criar **Webhook Handler** para receber mensagens
4. Criar **endpoint FastAPI** para o webhook

---

## 📋 Parte 1: Alembic (Migrations)

### O que é Alembic?

**Alembic** é a ferramenta de migrations do SQLAlchemy:
- Versiona mudanças no schema do banco
- Permite aplicar/reverter alterações
- Gera scripts automaticamente

### Estrutura de Arquivos

```
alembic/
├── env.py              # Carrega models e configura conexão
├── script.py.mako      # Template para novas migrations
└── versions/
    └── 001_initial_tables.py  # Migration inicial
```

### Comandos Principais

```bash
# Criar nova migration
alembic revision -m "add_column_x"

# Aplicar todas as migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Ver histórico
alembic history
```

### Anatomia de uma Migration

```python
def upgrade() -> None:
    """Aplica as mudanças."""
    op.create_table(
        "customers",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("phone_number", sa.String(15), unique=True),
    )

def downgrade() -> None:
    """Reverte as mudanças."""
    op.drop_table("customers")
```

---

## 📋 Parte 2: WhatsApp Client

### Conceito

Cliente HTTP assíncrono para enviar mensagens via WhatsApp Cloud API.

### Uso

```python
async with WhatsAppClient() as client:
    # Texto simples
    await client.send_text_message(
        to="5511999999999",
        text="Olá! Como posso ajudar?"
    )
    
    # Mensagem com botões
    await client.send_reply_button_message(
        to="5511999999999",
        body_text="Escolha uma opção:",
        buttons=[
            {"id": "opt_1", "title": "Ver produtos"},
            {"id": "opt_2", "title": "Meus pedidos"},
        ]
    )
```

### Métodos Disponíveis

| Método | Descrição |
|--------|-----------|
| `send_text_message()` | Envia texto simples |
| `send_reply_button_message()` | Envia com botões (max 3) |
| `send_list_message()` | Envia menu em lista |
| `mark_as_read()` | Marca como lida |

---

## 📋 Parte 3: Webhook Handler

### Conceito

Processa requisições do WhatsApp:
- **GET**: Verificação inicial do webhook
- **POST**: Receber mensagens

### Verificação do Webhook

```python
handler = WebhookHandler()

success, challenge = handler.verify_webhook(
    mode="subscribe",
    token="meu_token",
    challenge="abc123"
)
```

### Extração de Mensagem

```python
message_data = handler.extract_message_data(payload)
# Retorna:
# {
#     "from": "5511999999999",
#     "message_id": "wamid.xxx",
#     "type": "text",
#     "text": "Olá!",
# }
```

---

## 📋 Parte 4: Endpoint FastAPI

### Rotas Criadas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/webhook` | Verificação do Meta |
| POST | `/webhook` | Receber mensagens |

### Fluxo de Mensagem

```
1. WhatsApp envia POST → /webhook
2. Valida assinatura HMAC
3. Extrai dados da mensagem
4. Processa em background (BackgroundTasks)
5. Retorna 200 OK imediatamente
```

---

## ✅ Verificação da Fase 6

```bash
# Testar imports
python -c "from src.infrastructure.whatsapp import WhatsAppClient, WebhookHandler"

# Rodar testes WhatsApp
pytest tests/unit/infrastructure/whatsapp/ -v

# Resultado: 14 passed
# Total: 108 passed, 80% coverage
```

---

## ✅ Checklist da Fase 6

- [x] Criar alembic.ini
- [x] Criar alembic/env.py
- [x] Criar migration 001_initial_tables.py
- [x] Criar WhatsAppClient (4 métodos)
- [x] Criar WebhookHandler (4 métodos)
- [x] Criar endpoint /webhook (GET + POST)
- [x] Criar 14 testes unitários
- [x] 108 testes passando no total
- [x] 80% de cobertura

---

## 📚 Conceitos Aprendidos

| Conceito | Descrição |
|----------|-----------|
| `alembic` | Ferramenta de migrations |
| `op.create_table()` | Cria tabela no banco |
| `httpx.AsyncClient` | Cliente HTTP async |
| `BackgroundTasks` | Processamento em background no FastAPI |
| `HMAC` | Assinatura para validar origem |
| `PlainTextResponse` | Resposta texto para webhook |

---

## ➡️ Próxima Fase
---

*Documento atualizado em: Fevereiro 2026*
*Fase 6 concluída com sucesso!*

---

# 🚀 FASE 7: Handler Conectando Tudo

## 🎯 Objetivo da Fase 7

Conectar todos os componentes em um fluxo completo:
1. Criar **main.py** (app FastAPI)
2. Criar **MessageHandler** (orquestra o fluxo)
3. Configurar **Dependency Injection**

---

## 📋 Parte 1: main.py (App FastAPI)

### Estrutura

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info("🚀 Iniciando app...")
    yield
    # SHUTDOWN
    logger.info("👋 Encerrando app...")

app = FastAPI(
    title="whatsapp-ecommerce-bot",
    lifespan=lifespan,
)
```

### Como Rodar

```bash
uvicorn src.main:app --reload
```

---

## 📋 Parte 2: MessageHandler

### Conceito

Orquestra o fluxo completo:

```
Webhook → MessageHandler → UseCase → WhatsAppClient
```

### Uso

```python
handler = MessageHandler(
    customer_repo=repo1,
    session_repo=repo2,
    product_repo=repo3,
    order_repo=repo4,
)

await handler.handle(message_data)
```

---

## 📋 Parte 3: Dependency Injection

### O que é?

Dependências são "injetadas" de fora, não criadas internamente:

```python
# SEM DI (acoplado)
class Handler:
    def __init__(self):
        self.repo = SQLAlchemyRepo()  # ❌ Acoplado

# COM DI (desacoplado)
class Handler:
    def __init__(self, repo: IRepository):  # ✅ Injetado
        self.repo = repo
```

### No FastAPI

```python
from fastapi import Depends

@app.get("/users")
async def get_users(
    db: AsyncSession = Depends(get_db_session)
):
    ...
```

---

## ✅ Checklist da Fase 7

- [x] Criar src/main.py
- [x] Criar src/presentation/whatsapp/handler.py
- [x] Criar src/presentation/api/dependencies.py
- [x] Atualizar webhook para usar handler
- [x] 108 testes passando

---

## 📚 Conceitos Aprendidos

| Conceito | Descrição |
|----------|-----------|
| `lifespan` | Gerencia startup/shutdown |
| `@lru_cache` | Singleton para DI |
| `Depends()` | Injeção no FastAPI |
| `BackgroundTasks` | Processamento async |

---
---

*Documento atualizado em: Fevereiro 2026*
*Fase 7 concluída com sucesso!*

---

# 🚀 FASE 8: Testes de Integração

## 🎯 Objetivo da Fase 8

Criar testes que verificam componentes combinados:
1. Testes de endpoints FastAPI
2. Fluxo completo webhook → resposta

---

## 📋 TestClient do FastAPI

### Conceito

Cliente de teste que simula requisições HTTP:
- Executa em memória (sem servidor real)
- Suporta GET, POST, PUT, DELETE
- Acessa response.json() diretamente

### Uso

```python
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
```

---

## ✅ Testes Criados

| Classe | Testes | Descrição |
|--------|--------|-----------|
| TestHealthCheck | 3 | Endpoint /health |
| TestRootEndpoint | 2 | Endpoint / |
| TestWebhookVerification | 3 | GET /webhook |
| TestWebhookPost | 3 | POST /webhook |

---

## ✅ Checklist da Fase 8

- [x] Criar tests/integration/test_api.py
- [x] 11 testes de integração passando
- [x] 119 testes no total (108 + 11)
- [x] Fluxo webhook testado

---
---

*Documento atualizado em: Fevereiro 2026*
*Fase 8 concluída com sucesso!*

---

# 🚀 FASE 9: Docker e Deploy

## 🎯 Objetivo da Fase 9

Containerizar a aplicação para deploy:
1. Criar **Dockerfile** otimizado
2. Criar **docker-compose.yml** com todos os serviços
3. Documentar o processo de deploy

---

## 📋 Dockerfile (Multi-stage Build)

### Conceito

Multi-stage build cria imagens menores e mais seguras:
- **Stage 1 (builder):** Instala dependências
- **Stage 2 (runtime):** Imagem final sem ferramentas de build

### Comandos

```bash
# Build da imagem
docker build -t whatsapp-bot .

# Rodar container
docker run -p 8000:8000 whatsapp-bot
```

---

## 📋 Docker Compose

### Serviços

| Serviço | Imagem | Porta |
|---------|--------|-------|
| app | whatsapp-bot | 8000 |
| postgres | postgres:16-alpine | 5432 |
| redis | redis:7-alpine | 6379 |

### Comandos

```bash
# Subir todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Parar tudo
docker-compose down

# Rebuild após mudanças
docker-compose up -d --build
```

---

## ✅ Checklist da Fase 9

- [x] Criar Dockerfile (multi-stage)
- [x] Criar docker-compose.yml
- [x] Criar .dockerignore
- [x] Health checks configurados

---

# 🎉 PROJETO COMPLETO!

## Resumo Final

| Fase | Status | Descrição |
|------|--------|-----------|
| 0 | ✅ | Setup do Ambiente |
| 1 | ✅ | Estrutura Base |
| 2 | ✅ | Entidades (Domain) |
| 3 | ✅ | Repositórios (Interfaces) |
| 4 | ✅ | Use Cases (Application) |
| 5 | ✅ | Database (Infrastructure) |
| 6 | ✅ | WhatsApp (Integration) |
| 7 | ✅ | Handler (Orchestration) |
| 8 | ✅ | Testes de Integração |
| 9 | ✅ | Docker e Deploy |

## Estatísticas

- **Arquivos Python:** 43+
- **Testes:** 119
- **Cobertura:** ~70%
- **Fases Completas:** 10/10

---

*Documento finalizado em: Fevereiro 2026*
*Projeto WhatsApp E-commerce Bot concluído com sucesso!*
