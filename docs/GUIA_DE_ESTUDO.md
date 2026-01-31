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
