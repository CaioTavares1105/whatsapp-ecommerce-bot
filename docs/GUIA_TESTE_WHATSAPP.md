# GUIA DE TESTE NO WHATSAPP

## Como Testar o Chatbot no Seu WhatsApp Real

**Tempo estimado:** 30-45 minutos

---

# SUMÁRIO

1. [Pré-requisitos](#1-pré-requisitos)
2. [Criar Conta Meta Business](#2-criar-conta-meta-business)
3. [Configurar WhatsApp Business API](#3-configurar-whatsapp-business-api)
4. [Obter Tokens](#4-obter-tokens)
5. [Configurar .env](#5-configurar-env)
6. [Instalar e Rodar ngrok](#6-instalar-e-rodar-ngrok)
7. [Configurar Webhook no Meta](#7-configurar-webhook-no-meta)
8. [Rodar o Servidor](#8-rodar-o-servidor)
9. [Testar no WhatsApp](#9-testar-no-whatsapp)
10. [Troubleshooting](#10-troubleshooting)

---

# 1. PRÉ-REQUISITOS

## O que você precisa ter:

| Item | Status |
|------|--------|
| Conta Facebook pessoal | ⬜ |
| Número de telefone (para verificação) | ⬜ |
| Docker Desktop instalado | ⬜ |
| Python 3.12+ instalado | ⬜ |
| Git instalado | ⬜ |

## Verificar instalações:

```bash
# Python
python --version
# Esperado: Python 3.12.x

# Docker
docker --version
# Esperado: Docker version 24.x.x

# Git
git --version
# Esperado: git version 2.x.x
```

---

# 2. CRIAR CONTA META BUSINESS

## Passo 2.1: Acessar Meta for Developers

1. Acesse: **https://developers.facebook.com/**
2. Clique em **"Começar"** ou **"Get Started"**
3. Faça login com sua conta Facebook

## Passo 2.2: Criar conta de desenvolvedor

1. Aceite os termos de uso
2. Verifique seu email
3. Complete o cadastro

## Passo 2.3: Criar um App

1. Clique em **"Meus Apps"** (My Apps)
2. Clique em **"Criar App"** (Create App)
3. Selecione **"Outros"** (Other) como tipo
4. Escolha **"Business"** como tipo de app
5. Dê um nome: `WhatsApp Chatbot Test`
6. Clique em **"Criar App"**

```
┌─────────────────────────────────────────────────────────────────┐
│                    PAINEL META DEVELOPERS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Meus Apps  →  [Criar App]                                      │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Nome do App: WhatsApp Chatbot Test                       │  │
│  │  Tipo: Business                                           │  │
│  │  Conta Business: (selecione ou crie)                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│                              [Criar App]                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

# 3. CONFIGURAR WHATSAPP BUSINESS API

## Passo 3.1: Adicionar produto WhatsApp

1. No painel do seu App, encontre **"Adicionar produtos"**
2. Procure por **"WhatsApp"**
3. Clique em **"Configurar"**

## Passo 3.2: Aceitar termos

1. Aceite os termos do WhatsApp Business Platform
2. Selecione sua conta Business (ou crie uma)

## Passo 3.3: Número de teste

O Meta fornece um **número de teste gratuito** para desenvolvimento:
- Você pode enviar mensagens para números verificados
- Limite: 5 números de telefone por dia

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHATSAPP > API SETUP                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Número de telefone de teste: +1 555 XXX XXXX                   │
│                                                                  │
│  Para testar, adicione seu número:                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Seu número: +55 11 99999-9999                            │  │
│  │                                      [Adicionar]          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Números verificados:                                            │
│  • +55 11 99999-9999 ✓                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

# 4. OBTER TOKENS

## Passo 4.1: Access Token (Temporário)

1. Na página **WhatsApp > API Setup**
2. Localize **"Temporary access token"**
3. Clique em **"Copy"**

⚠️ **IMPORTANTE:** Este token expira em 24 horas. Para produção, você precisará de um token permanente.

## Passo 4.2: Phone Number ID

1. Na mesma página, localize **"Phone number ID"**
2. Copie o valor (algo como: `123456789012345`)

## Passo 4.3: Verify Token (você cria)

1. Este token você **inventa**
2. Use algo aleatório, ex: `meu_token_secreto_123`
3. Guarde para usar na configuração do webhook

## Passo 4.4: App Secret

1. Vá para **Configurações > Básico**
2. Localize **"Chave Secreta do App"**
3. Clique em **"Mostrar"**
4. Copie o valor

```
┌─────────────────────────────────────────────────────────────────┐
│                      TOKENS OBTIDOS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Access Token:      EAAGxxxx...xxxxx (temporário 24h)           │
│  Phone Number ID:   123456789012345                              │
│  Verify Token:      meu_token_secreto_123 (você cria)           │
│  App Secret:        abc123def456... (Configurações > Básico)     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

# 5. CONFIGURAR .ENV

## Passo 5.1: Editar arquivo .env

Abra o arquivo `.env` na raiz do projeto e preencha:

```bash
# ===== CONFIGURAÇÃO DO APP =====
APP_NAME=whatsapp-ecommerce-bot
APP_ENV=development
DEBUG=true
SECRET_KEY=sua-chave-secreta-qualquer-123

# ===== BANCO DE DADOS =====
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/chatbot_db

# ===== REDIS =====
REDIS_URL=redis://localhost:6379/0

# ===== WHATSAPP (PREENCHA COM SEUS TOKENS) =====
WHATSAPP_API_TOKEN=EAAGxxxx...seu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_VERIFY_TOKEN=meu_token_secreto_123
WHATSAPP_WEBHOOK_SECRET=abc123def456...seu_app_secret

# ===== API =====
API_HOST=0.0.0.0
API_PORT=8000

# ===== LOGS =====
LOG_LEVEL=DEBUG
```

## Passo 5.2: Verificar configuração

```bash
# No terminal, na pasta do projeto
python -c "from src.config.settings import get_settings; s = get_settings(); print(f'Token: {s.whatsapp_api_token[:20]}...')"
```

Se aparecer parte do seu token, está configurado!

---

# 6. INSTALAR E RODAR NGROK

## Por que ngrok?

O WhatsApp precisa enviar mensagens para o seu servidor. Mas seu computador está "escondido" atrás de um roteador. O **ngrok cria um túnel** que expõe seu localhost para a internet.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   SEM ngrok:                                                     │
│                                                                  │
│   WhatsApp ──X──▶ localhost:8000  (não consegue acessar)        │
│                                                                  │
│   COM ngrok:                                                     │
│                                                                  │
│   WhatsApp ──▶ https://abc123.ngrok.io ──▶ localhost:8000       │
│                           │                                      │
│                    (túnel público)                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Passo 6.1: Criar conta ngrok

1. Acesse: **https://ngrok.com/**
2. Clique em **"Sign up"**
3. Crie conta (pode usar GitHub)

## Passo 6.2: Instalar ngrok

### Windows (via Chocolatey):
```bash
choco install ngrok
```

### Windows (download manual):
1. Baixe de: https://ngrok.com/download
2. Extraia o ZIP
3. Adicione ao PATH ou coloque na pasta do projeto

### Linux/Mac:
```bash
# Mac
brew install ngrok

# Linux
snap install ngrok
```

## Passo 6.3: Autenticar ngrok

1. No site do ngrok, vá em **"Your Authtoken"**
2. Copie o token
3. No terminal:

```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```

## Passo 6.4: Rodar ngrok

```bash
ngrok http 8000
```

Você verá algo assim:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  ngrok                                                           │
│                                                                  │
│  Session Status    online                                        │
│  Account           seu@email.com                                 │
│  Version           3.x.x                                         │
│  Region            United States (us)                            │
│  Forwarding        https://abc123.ngrok.io -> localhost:8000    │
│                    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑                     │
│                    COPIE ESTA URL!                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**COPIE a URL https://xxxxx.ngrok.io** - você vai usar no próximo passo!

---

# 7. CONFIGURAR WEBHOOK NO META

## Passo 7.1: Acessar configuração do Webhook

1. No painel do Meta Developers
2. Vá para **WhatsApp > Configuração**
3. Localize a seção **"Webhook"**

## Passo 7.2: Configurar URL do Webhook

1. Clique em **"Editar"** no Webhook
2. Preencha:
   - **URL de retorno:** `https://SEU-NGROK.ngrok.io/webhook`
   - **Token de verificação:** `meu_token_secreto_123` (o que você colocou no .env)

## Passo 7.3: Verificar webhook

1. Clique em **"Verificar e salvar"**
2. O Meta vai enviar uma requisição GET para sua URL
3. Se tudo estiver correto, aparece ✓ verde

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIGURAR WEBHOOK                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  URL de retorno de chamada:                                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  https://abc123.ngrok.io/webhook                          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Token de verificação:                                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  meu_token_secreto_123                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│                     [Verificar e salvar]                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Passo 7.4: Assinar campos de webhook

Após verificar, você precisa **assinar os campos** para receber mensagens:

1. Na seção **"Campos do Webhook"**
2. Clique em **"Gerenciar"**
3. Marque: ✅ **messages**
4. Clique em **"Concluído"**

---

# 8. RODAR O SERVIDOR

## Passo 8.1: Subir banco e redis (Docker)

Abra um terminal e rode:

```bash
cd "C:\Users\User\Desktop\WhatsApp chatBot"
docker-compose up postgres redis -d
```

Aguarde inicializar (30 segundos).

## Passo 8.2: Aplicar migrations

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Rodar migrations
alembic upgrade head
```

## Passo 8.3: Rodar servidor FastAPI

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Você deve ver:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

## Passo 8.4: Testar localmente

Abra o navegador: **http://localhost:8000/health**

Deve retornar:
```json
{"status": "healthy"}
```

---

# 9. TESTAR NO WHATSAPP

## Passo 9.1: Verificar tudo rodando

```
┌────────────────────────────────────────────────────────────────┐
│                    CHECKLIST FINAL                              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Terminal 1: docker-compose up postgres redis -d    ✓ rodando  │
│  Terminal 2: ngrok http 8000                        ✓ rodando  │
│  Terminal 3: uvicorn src.main:app --reload          ✓ rodando  │
│                                                                 │
│  Meta webhook: configurado com URL do ngrok         ✓ verde    │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Passo 9.2: Enviar mensagem teste

1. Abra o **WhatsApp** no seu celular
2. Adicione o número de teste do Meta como contato
3. Envie: **"Olá"**

## Passo 9.3: O que esperar

```
┌────────────────────────────────────────────────────────────────┐
│                        WHATSAPP                                 │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Você:                                                          │
│  ┌─────────────────────────────────┐                           │
│  │ Olá                              │                           │
│  └─────────────────────────────────┘                           │
│                                                                 │
│                                           Bot:                  │
│                           ┌─────────────────────────────────┐  │
│                           │ Olá! 👋 Bem-vindo à nossa loja! │  │
│                           │                                  │  │
│                           │ Como posso ajudar você hoje?    │  │
│                           │                                  │  │
│                           │ 1️⃣ Ver produtos                  │  │
│                           │ 2️⃣ Rastrear pedido               │  │
│                           │ 3️⃣ Dúvidas frequentes            │  │
│                           │ 4️⃣ Falar com atendente           │  │
│                           └─────────────────────────────────┘  │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Passo 9.4: Verificar logs

No terminal do uvicorn, você deve ver:

```
INFO:     POST /webhook - 200 OK
INFO:     Processing message from 5511999999999
INFO:     Intent identified: greeting
INFO:     Sending response to 5511999999999
```

---

# 10. TROUBLESHOOTING

## Problema: Webhook retorna 403

**Causa:** Verify token não bate.

**Solução:**
1. Verifique se `WHATSAPP_VERIFY_TOKEN` no .env é igual ao configurado no Meta
2. Reinicie o servidor

---

## Problema: Webhook verifica mas não recebe mensagens

**Causa:** Campo `messages` não está assinado.

**Solução:**
1. Vá em WhatsApp > Configuração
2. Webhook > Gerenciar
3. Marque ✅ messages
4. Salve

---

## Problema: ngrok URL mudou

**Causa:** ngrok gratuito muda a URL ao reiniciar.

**Solução:**
1. Copie a nova URL do ngrok
2. Atualize no Meta Developers
3. Verifique novamente

---

## Problema: Mensagem não chega

**Diagnóstico:**

```bash
# 1. Verificar se webhook está respondendo
curl https://SEU-NGROK.ngrok.io/health

# 2. Ver logs do uvicorn
# Deve mostrar requisições POST /webhook

# 3. Ver logs do ngrok (interface web)
# Acesse: http://localhost:4040
```

---

## Problema: Erro de banco de dados

```
sqlalchemy.exc.OperationalError: connection refused
```

**Solução:**

```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Se não estiver:
docker-compose up postgres redis -d

# Aguardar 30 segundos e tentar novamente
```

---

## Problema: Token expirado

```
WhatsApp API Error: Invalid OAuth access token
```

**Solução:**
1. Gere novo token temporário no Meta Developers
2. Atualize no .env
3. Reinicie o servidor

---

# RESUMO RÁPIDO

```bash
# 1. Subir banco
docker-compose up postgres redis -d

# 2. Rodar migrations
alembic upgrade head

# 3. Abrir túnel (outro terminal)
ngrok http 8000

# 4. Atualizar webhook no Meta com URL do ngrok

# 5. Rodar servidor (outro terminal)
uvicorn src.main:app --reload

# 6. Enviar "Olá" no WhatsApp
```

---

# PRÓXIMOS PASSOS

Após testar com sucesso:
1. ✅ Testar diferentes intenções (produtos, pedido, ajuda)
2. ✅ Verificar logs de debugging
3. ✅ Fazer a prova de 30 questões

---

**Parabéns! Seu chatbot está funcionando!** 🎉
