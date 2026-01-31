# 🤖 WhatsApp E-commerce Bot

> Chatbot inteligente para WhatsApp voltado para e-commerce, construído com Python, FastAPI e Clean Architecture.

## 📋 Descrição

Este projeto implementa um chatbot para WhatsApp Business que automatiza o atendimento ao cliente em lojas virtuais. O bot pode:

- 🛒 Mostrar catálogo de produtos
- 📦 Consultar status de pedidos
- ❓ Responder perguntas frequentes (FAQ)
- 👤 Transferir para atendente humano quando necessário

## 🛠️ Tecnologias

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.12+ | Linguagem principal |
| FastAPI | 0.109+ | Framework Web/API |
| SQLAlchemy | 2.x | ORM para banco de dados |
| PostgreSQL | 16 | Banco de dados |
| Redis | 7.x | Cache e sessões |
| pytest | 8.x | Testes |
| UV | Latest | Gerenciador de pacotes |

## 📁 Estrutura do Projeto

```
whatsapp-ecommerce-bot/
├── src/
│   ├── domain/          # Entidades e lógica de negócio
│   ├── application/     # Casos de uso
│   ├── infrastructure/  # Banco, cache, WhatsApp
│   └── presentation/    # API e handlers
├── tests/               # Testes automatizados
├── docs/                # Documentação
└── docker/              # Configuração Docker
```

## 🚀 Como Executar

### Pré-requisitos

1. Python 3.12+ 
2. UV (gerenciador de pacotes)
3. Docker Desktop
4. Git

### Instalação

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/whatsapp-ecommerce-bot.git
cd whatsapp-ecommerce-bot

# Criar ambiente virtual
python -m uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependências
python -m uv pip install -e ".[dev]"

# Copiar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Executar
python main.py
```

## 📖 Documentação

Consulte o arquivo `claude.md` para documentação completa do projeto.

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src
```

## 📝 Licença

Este projeto é para fins educacionais.

---

**Desenvolvido para aprender Python e Clean Architecture** 🐍
