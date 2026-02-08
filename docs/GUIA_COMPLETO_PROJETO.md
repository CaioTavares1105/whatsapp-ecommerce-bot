# GUIA COMPLETO DO PROJETO: WhatsApp E-commerce Bot

## Manual Didático para Desenvolvedores

**Autor:** Professor Claude (Dev Senior)
**Versão:** 1.0
**Data:** Fevereiro 2026

---

# SUMÁRIO

1. [PARTE 1: FUNDAMENTOS](#parte-1-fundamentos)
2. [PARTE 2: FASES DO PROJETO](#parte-2-fases-do-projeto)
3. [PARTE 3: DEBUGGING](#parte-3-debugging)
4. [PARTE 4: DIAGRAMAS](#parte-4-diagramas)

---

# PARTE 1: FUNDAMENTOS

## 1.1 O que é Python?

### Explicação Simples (como para uma criança)

Imagine que você quer dar instruções para um robô fazer um bolo. Você precisa falar em uma língua que ele entenda. **Python é essa língua!**

```
PORTUGUÊS:                    PYTHON:
"Pegue 2 ovos"        →      ovos = 2
"Misture com farinha" →      mistura = ovos + farinha
"Se estiver bom..."   →      if mistura == "boa":
"...coloque no forno" →          forno.assar(mistura)
```

### Por que Python?

| Característica | Benefício |
|----------------|-----------|
| Sintaxe limpa | Código parece inglês |
| Tipagem opcional | Pode usar type hints |
| Muitas bibliotecas | FastAPI, SQLAlchemy, etc. |
| Comunidade grande | Fácil encontrar ajuda |

---

## 1.2 O que é Git?

### Explicação Simples

Git é como um **Ctrl+Z infinito** para seu código. Mas melhor!

```
┌─────────────────────────────────────────────────────────────┐
│                      LINHA DO TEMPO                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Versão 1      Versão 2      Versão 3      Versão 4         │
│     ●────────────●────────────●────────────●                │
│     │            │            │            │                 │
│   "Início"   "Adiciona    "Corrige     "Adiciona            │
│              login"       bug"         carrinho"            │
│                                                              │
│  Você pode VOLTAR para qualquer versão a qualquer momento!  │
└─────────────────────────────────────────────────────────────┘
```

### Comandos Essenciais

| Comando | O que faz | Analogia |
|---------|-----------|----------|
| `git add .` | Prepara arquivos | Colocar na caixa |
| `git commit -m "msg"` | Salva versão | Fechar e etiquetar caixa |
| `git push` | Envia para nuvem | Enviar caixa pelo correio |
| `git pull` | Baixa da nuvem | Receber caixa |
| `git status` | Mostra situação | Verificar o que mudou |

---

## 1.3 O que é Clean Architecture?

### Explicação Simples

Imagine uma **cebola com 4 camadas**. Cada camada tem uma responsabilidade:

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│    ┌─────────────────────────────────────────────────────┐  │
│    │                   PRESENTATION                       │  │
│    │              (Interface com usuário)                 │  │
│    │    ┌─────────────────────────────────────────────┐  │  │
│    │    │              APPLICATION                     │  │  │
│    │    │           (Orquestra tudo)                  │  │  │
│    │    │    ┌─────────────────────────────────────┐  │  │  │
│    │    │    │            DOMAIN                    │  │  │  │
│    │    │    │    (Regras de negócio)              │  │  │  │
│    │    │    │    ┌─────────────────────────────┐  │  │  │  │
│    │    │    │    │      INFRASTRUCTURE         │  │  │  │  │
│    │    │    │    │   (Banco, APIs externas)    │  │  │  │  │
│    │    │    │    └─────────────────────────────┘  │  │  │  │
│    │    │    └─────────────────────────────────────┘  │  │  │
│    │    └─────────────────────────────────────────────┘  │  │
│    └─────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Por que separar em camadas?

| Problema SEM camadas | Solução COM camadas |
|----------------------|---------------------|
| Código misturado | Cada arquivo tem UMA responsabilidade |
| Difícil testar | Pode testar cada parte separada |
| Difícil trocar banco | Troca só a camada de infra |
| Um bug afeta tudo | Bug fica isolado na camada |

### Regra de Ouro: Dependência para DENTRO

```
PRESENTATION → APPLICATION → DOMAIN ← INFRASTRUCTURE

✅ Presentation PODE importar Application
✅ Application PODE importar Domain
✅ Infrastructure IMPLEMENTA Domain
❌ Domain NÃO importa ninguém (é o núcleo!)
```

---

## 1.4 Fluxo de uma Mensagem WhatsApp

```
┌─────────────────────────────────────────────────────────────────┐
│                    JORNADA DA MENSAGEM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. USUÁRIO                                                      │
│     📱 Digita "Olá" no WhatsApp                                  │
│         │                                                        │
│         ▼                                                        │
│  2. META (Facebook)                                              │
│     ☁️  Recebe mensagem e envia para seu servidor               │
│         │                                                        │
│         ▼                                                        │
│  3. WEBHOOK (seu servidor)                                       │
│     🔒 Valida assinatura HMAC (é realmente do WhatsApp?)        │
│         │                                                        │
│         ▼                                                        │
│  4. HANDLER                                                      │
│     📦 Extrai dados: telefone, texto, timestamp                 │
│         │                                                        │
│         ▼                                                        │
│  5. USE CASE                                                     │
│     🧠 Processa: "Olá" → intenção GREETING → menu               │
│         │                                                        │
│         ▼                                                        │
│  6. WHATSAPP CLIENT                                              │
│     📤 Envia resposta via API                                   │
│         │                                                        │
│         ▼                                                        │
│  7. USUÁRIO                                                      │
│     📱 Recebe "Bem-vindo! Como posso ajudar?"                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

# PARTE 2: FASES DO PROJETO

---

## FASE 0: Setup do Ambiente

### O que foi feito
Configuração inicial do ambiente de desenvolvimento.

### Como foi feito

```bash
# 1. Criar pasta do projeto
mkdir whatsapp-ecommerce-bot
cd whatsapp-ecommerce-bot

# 2. Inicializar Git
git init

# 3. Criar ambiente virtual Python
uv venv
.venv\Scripts\activate  # Windows

# 4. Definir versão Python
echo "3.12" > .python-version
```

### Por que foi feito

| Ação | Motivo |
|------|--------|
| `git init` | Controlar versões do código |
| `uv venv` | Isolar dependências do projeto |
| `.python-version` | Garantir mesma versão para todos |

### Arquivos Criados

```
whatsapp-ecommerce-bot/
├── .git/              ← Pasta do Git (oculta)
├── .venv/             ← Ambiente virtual Python
├── .gitignore         ← Arquivos ignorados pelo Git
├── .python-version    ← Versão do Python
└── pyproject.toml     ← Configuração do projeto
```

### Diagrama do Fluxo Git

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  WORKING DIR    │     │   STAGING       │     │   REPOSITORY    │
│  (seus arquivos)│     │   (preparados)  │     │   (salvos)      │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │    git add .          │                       │
         │──────────────────────▶│                       │
         │                       │                       │
         │                       │    git commit -m ""   │
         │                       │──────────────────────▶│
         │                       │                       │
         │                       │                       │   git push
         │                       │                       │──────────▶ GitHub
```

---

## FASE 1: Estrutura Base

### O que foi feito
Criação da estrutura de pastas seguindo Clean Architecture.

### Como foi feito

```bash
# Criar todas as pastas
mkdir -p src/{domain/{entities,repositories,services},application/{usecases,dtos},infrastructure/{database/repositories,cache,whatsapp},presentation/{api/routes,whatsapp},config,shared/{errors,utils,types}}
```

### Estrutura Final

```
src/
├── domain/                    ← CAMADA DE DOMÍNIO (núcleo)
│   ├── entities/              ← Objetos de negócio
│   │   ├── customer.py        ← Cliente
│   │   ├── product.py         ← Produto
│   │   ├── order.py           ← Pedido
│   │   └── session.py         ← Sessão de chat
│   ├── repositories/          ← Interfaces (contratos)
│   │   ├── customer_repository.py
│   │   ├── product_repository.py
│   │   └── order_repository.py
│   └── services/              ← Lógica de domínio
│
├── application/               ← CAMADA DE APLICAÇÃO
│   ├── usecases/              ← Casos de uso
│   │   └── handle_message.py  ← Processa mensagens
│   └── dtos/                  ← Objetos de transferência
│       └── message_dto.py
│
├── infrastructure/            ← CAMADA DE INFRAESTRUTURA
│   ├── database/              ← Banco de dados
│   │   ├── models.py          ← Tabelas SQL
│   │   ├── connection.py      ← Conexão
│   │   └── repositories/      ← Implementações
│   ├── whatsapp/              ← Integração WhatsApp
│   │   ├── client.py          ← Envia mensagens
│   │   └── webhook.py         ← Recebe mensagens
│   └── cache/                 ← Redis (cache)
│
├── presentation/              ← CAMADA DE APRESENTAÇÃO
│   ├── api/                   ← API REST (FastAPI)
│   │   ├── routes/
│   │   │   └── webhook.py     ← Endpoints
│   │   └── dependencies.py    ← Injeção de dependência
│   └── whatsapp/
│       └── handler.py         ← Processa webhooks
│
├── config/                    ← CONFIGURAÇÕES
│   └── settings.py            ← Variáveis de ambiente
│
└── shared/                    ← COMPARTILHADO
    ├── types/
    │   └── enums.py           ← Enumerações
    └── errors/
        └── exceptions.py      ← Exceções customizadas
```

### Por que esta estrutura?

| Pasta | Responsabilidade | Exemplo |
|-------|------------------|---------|
| `domain/` | Regras de negócio puras | "Cliente deve ter telefone válido" |
| `application/` | Orquestrar operações | "Quando chega mensagem, faça X, Y, Z" |
| `infrastructure/` | Detalhes técnicos | "Salvar no PostgreSQL" |
| `presentation/` | Interface externa | "Receber POST /webhook" |

---

## FASE 2: Entidades de Domínio

### O que foi feito
Criação das 4 entidades principais do negócio.

### Arquivos

| Arquivo | Entidade | Responsabilidade |
|---------|----------|------------------|
| `customer.py` | Customer | Dados do cliente |
| `product.py` | Product | Dados do produto |
| `order.py` | Order | Dados do pedido |
| `session.py` | Session | Sessão de conversa |

### Como foi feito: Customer

```python
# src/domain/entities/customer.py

from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass  # ← Gera __init__, __repr__, __eq__ automaticamente
class Customer:
    """
    Entidade que representa um cliente.

    REGRAS DE NEGÓCIO:
    - Telefone deve ter 10-15 dígitos
    - Telefone é único (identificador)
    """

    # Atributos OBRIGATÓRIOS (sem valor padrão)
    phone_number: str

    # Atributos OPCIONAIS (com valor padrão)
    name: str | None = None  # ← Python 3.10+: str ou None
    email: str | None = None

    # Atributos com FACTORY (gerados automaticamente)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """
        Executado APÓS __init__.
        Usado para validações.
        """
        self._validate_phone_number()

    def _validate_phone_number(self) -> None:
        """Valida e limpa o telefone."""
        # Remove caracteres não numéricos
        clean_phone = "".join(filter(str.isdigit, self.phone_number))

        if len(clean_phone) < 10 or len(clean_phone) > 15:
            raise ValueError(f"Telefone inválido: {self.phone_number}")

        self.phone_number = clean_phone  # Salva limpo
```

### Conceitos Python Explicados

#### 1. @dataclass

```python
# SEM @dataclass (manual)
class Customer:
    def __init__(self, phone, name=None):
        self.phone = phone
        self.name = name

    def __repr__(self):
        return f"Customer(phone={self.phone})"

    def __eq__(self, other):
        return self.phone == other.phone

# COM @dataclass (automático)
@dataclass
class Customer:
    phone: str
    name: str | None = None
# Python gera __init__, __repr__, __eq__ sozinho!
```

#### 2. field(default_factory=...)

```python
# ❌ ERRADO: Todos compartilham a MESMA lista!
@dataclass
class Carrinho:
    itens: list = []  # PERIGOSO!

# ✅ CORRETO: Cada instância tem lista própria
@dataclass
class Carrinho:
    itens: list = field(default_factory=list)
```

#### 3. str | None (Union Type)

```python
# Significa: pode ser str OU None
name: str | None = None

# Equivalente em versões antigas:
from typing import Optional
name: Optional[str] = None
```

### Diagrama: Entidades e Relacionamentos

```
┌─────────────────────────────────────────────────────────────────┐
│                      MODELO DE DOMÍNIO                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │   CUSTOMER   │         │   PRODUCT    │                      │
│  ├──────────────┤         ├──────────────┤                      │
│  │ id           │         │ id           │                      │
│  │ phone_number │         │ name         │                      │
│  │ name         │         │ price        │                      │
│  │ email        │         │ category     │                      │
│  │ created_at   │         │ stock        │                      │
│  └──────┬───────┘         │ active       │                      │
│         │                 └──────────────┘                      │
│         │ 1                                                     │
│         │                                                       │
│         │ N                                                     │
│  ┌──────┴───────┐         ┌──────────────┐                      │
│  │    ORDER     │         │   SESSION    │                      │
│  ├──────────────┤         ├──────────────┤                      │
│  │ id           │         │ id           │                      │
│  │ customer_id  │◄────────│ customer_id  │                      │
│  │ status       │         │ state        │                      │
│  │ total        │         │ context      │                      │
│  │ created_at   │         │ expires_at   │                      │
│  └──────────────┘         └──────────────┘                      │
│                                                                  │
│  LEGENDA:                                                        │
│  ─────────────                                                   │
│  1 → N  : Um cliente pode ter vários pedidos                    │
│  ◄────── : Referência (foreign key)                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## FASE 3: Interfaces de Repositório

### O que foi feito
Criação de contratos (interfaces) usando ABC.

### Por que usar interfaces?

**Analogia: Tomada Elétrica**

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   INTERFACE = Formato da Tomada                                 │
│   ════════════════════════════                                  │
│                                                                  │
│   ┌─────────┐                                                   │
│   │  ○   ○  │  ← Padrão: 2 pinos                               │
│   └─────────┘                                                   │
│                                                                  │
│   IMPLEMENTAÇÃO = Aparelho que encaixa                          │
│   ════════════════════════════════════                          │
│                                                                  │
│   ┌─────┐  ┌─────┐  ┌─────┐                                    │
│   │ TV  │  │ PC  │  │ 📱  │  ← Qualquer um que tenha           │
│   └─────┘  └─────┘  └─────┘    os 2 pinos funciona!            │
│                                                                  │
│   No código:                                                     │
│   - Interface = ICustomerRepository (define métodos)            │
│   - Implementação = SQLAlchemyCustomerRepository (faz de fato)  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Como foi feito

```python
# src/domain/repositories/customer_repository.py

from abc import ABC, abstractmethod  # ABC = Abstract Base Class

class ICustomerRepository(ABC):
    """
    Interface para repositório de clientes.

    "I" no início = Interface (convenção)
    ABC = Não pode ser instanciada diretamente
    @abstractmethod = Método DEVE ser implementado
    """

    @abstractmethod
    async def find_by_phone(self, phone: str) -> Customer | None:
        """Busca cliente por telefone."""
        ...  # ← Ellipsis: "será implementado depois"

    @abstractmethod
    async def save(self, customer: Customer) -> None:
        """Salva novo cliente."""
        ...

    @abstractmethod
    async def update(self, customer: Customer) -> None:
        """Atualiza cliente existente."""
        ...
```

### Conceitos Explicados

#### 1. ABC (Abstract Base Class)

```python
from abc import ABC, abstractmethod

class Animal(ABC):  # Não pode fazer: animal = Animal()

    @abstractmethod
    def fazer_som(self):
        ...

class Cachorro(Animal):  # DEVE implementar fazer_som
    def fazer_som(self):
        return "Au au!"

# ❌ animal = Animal()  # ERRO!
# ✅ dog = Cachorro()   # OK!
```

#### 2. Ellipsis (...)

```python
# ... significa "será implementado pela classe filha"
@abstractmethod
def metodo(self):
    ...  # Placeholder

# NÃO significa "aceita qualquer tipo"!
# É só um marcador visual.
```

#### 3. async/await

```python
# Função ASSÍNCRONA: não bloqueia enquanto espera
async def buscar_cliente(phone: str):
    cliente = await banco.query(phone)  # Espera sem travar
    return cliente

# Por que async?
# - Enquanto espera o banco, pode atender outras requisições
# - Essencial para APIs com muitos usuários simultâneos
```

---

## FASE 4: Casos de Uso

### O que foi feito
Implementação do `HandleMessageUseCase` - o "cérebro" do chatbot.

### Analogia: Maestro de Orquestra

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   USE CASE = MAESTRO                                            │
│   ══════════════════                                            │
│                                                                  │
│                      👨‍🎤 UseCase                                  │
│                         │                                        │
│          ┌──────────────┼──────────────┐                        │
│          │              │              │                         │
│          ▼              ▼              ▼                         │
│       🎻 Repo       🎺 Repo       🥁 Repo                        │
│       Customer      Session      Product                         │
│                                                                  │
│   O Maestro (UseCase) não toca nenhum instrumento.              │
│   Ele COORDENA os músicos (Repositories).                       │
│                                                                  │
│   - Não sabe SQL                                                │
│   - Não sabe HTTP                                               │
│   - Só sabe a ORDEM das operações                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Como foi feito

```python
# src/application/usecases/handle_message.py

class HandleMessageUseCase:
    """
    Caso de uso principal: processar mensagem do WhatsApp.

    FLUXO:
    1. Recebe mensagem
    2. Busca/cria cliente
    3. Busca/cria sessão
    4. Identifica intenção
    5. Gera resposta
    """

    def __init__(
        self,
        customer_repo: ICustomerRepository,  # ← Interface, não implementação!
        session_repo: ISessionRepository,
        product_repo: IProductRepository,
        order_repo: IOrderRepository,
    ) -> None:
        # Injeção de Dependência: recebe de fora
        self._customer_repo = customer_repo
        self._session_repo = session_repo
        self._product_repo = product_repo
        self._order_repo = order_repo

        # Palavras-chave para identificar intenções
        self._intent_keywords = {
            "greeting": ["oi", "olá", "bom dia"],
            "products": ["produto", "comprar", "preço"],
            "order_status": ["pedido", "rastreio"],
            "human": ["atendente", "humano"],
        }

    async def execute(self, input_dto: IncomingMessageDTO) -> MessageResponseDTO:
        """Executa o processamento."""

        # 1. Buscar ou criar cliente
        customer = await self._get_or_create_customer(input_dto.phone_number)

        # 2. Buscar ou criar sessão
        session = await self._get_or_create_session(customer.id)

        # 3. Identificar intenção
        intent = self._identify_intent(input_dto.text)

        # 4. Processar e gerar resposta
        response = await self._process_message(session, intent, input_dto.text)

        return response
```

### Conceitos Explicados

#### 1. Injeção de Dependência

```python
# ❌ ERRADO: UseCase cria suas dependências
class HandleMessageUseCase:
    def __init__(self):
        self.repo = SQLAlchemyCustomerRepository()  # Acoplado!

# ✅ CORRETO: UseCase RECEBE dependências
class HandleMessageUseCase:
    def __init__(self, repo: ICustomerRepository):  # Desacoplado!
        self.repo = repo

# Quem usa pode passar o que quiser:
# - Em produção: SQLAlchemyCustomerRepository
# - Em testes: MockCustomerRepository
```

#### 2. DTO (Data Transfer Object)

```python
# DTO = Envelope para transportar dados entre camadas

# Mensagem ENTRANDO
class IncomingMessageDTO(BaseModel):
    phone_number: str
    text: str

# Mensagem SAINDO
class MessageResponseDTO(BaseModel):
    text: str
    should_transfer_to_human: bool = False

# Por que usar DTO?
# - Entidade Customer tem 10 campos
# - Para responder, só preciso de 2
# - DTO carrega só o necessário
```

---

## FASE 5: Banco de Dados

### O que foi feito
Configuração do SQLAlchemy ORM com PostgreSQL.

### Analogia: Tradutor

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   ORM = TRADUTOR entre Python e SQL                             │
│   ═══════════════════════════════════                           │
│                                                                  │
│   PYTHON (você escreve)    →    SQL (banco entende)             │
│   ─────────────────────────────────────────────────             │
│   Customer(phone="123")    →    INSERT INTO customers...        │
│   repo.find_by_phone(x)    →    SELECT * FROM customers...      │
│   customer.name = "João"   →    UPDATE customers SET name...    │
│                                                                  │
│   Você NUNCA escreve SQL diretamente!                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Como foi feito: Models

```python
# src/infrastructure/database/models.py

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """Base para todos os modelos."""
    pass

class CustomerModel(Base):
    """
    Modelo SQLAlchemy = Tabela no banco.

    MAPEAMENTO:
    Classe Python  →  Tabela SQL
    Atributo       →  Coluna
    Instância      →  Linha
    """

    __tablename__ = "customers"  # Nome da tabela

    # Mapped[tipo] = define tipo Python E tipo SQL
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True  # Chave primária
    )

    phone_number: Mapped[str] = mapped_column(
        String(15),
        unique=True,      # Valor único
        index=True        # Cria índice (busca rápida)
    )

    name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True     # Pode ser NULL
    )
```

### Como foi feito: Connection

```python
# src/infrastructure/database/connection.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Engine = "Fábrica de conexões"
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=5,      # Mantém 5 conexões prontas
    max_overflow=10,  # Pode criar até 10 extras se precisar
)

# Session = "Conversa com o banco"
async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session  # FastAPI usa isso
```

### Diagrama: Engine vs Session

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   ENGINE = Restaurante                                          │
│   ════════════════════                                          │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    RESTAURANTE                           │   │
│   │                    (Engine)                              │   │
│   │                                                          │   │
│   │   ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐          │   │
│   │   │ Mesa 1 │ │ Mesa 2 │ │ Mesa 3 │ │ Mesa 4 │          │   │
│   │   │(Conn 1)│ │(Conn 2)│ │(Conn 3)│ │(Conn 4)│          │   │
│   │   └────────┘ └────────┘ └────────┘ └────────┘          │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   SESSION = Conversa numa mesa                                  │
│   ════════════════════════════                                  │
│                                                                  │
│   Cliente 1: "Quero ver cardápio" (SELECT)                      │
│   Cliente 1: "Vou pedir pizza" (INSERT)                         │
│   Cliente 1: "Conta por favor" (COMMIT)                         │
│   Cliente 1 vai embora, mesa fica livre para outro              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## FASE 6: Integração WhatsApp

### O que foi feito
Cliente HTTP para WhatsApp Cloud API + Webhook handler.

### Arquivos

| Arquivo | Responsabilidade |
|---------|------------------|
| `client.py` | ENVIA mensagens |
| `webhook.py` | RECEBE mensagens |

### Como funciona o Webhook

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   WEBHOOK = "Campainha" do seu servidor                         │
│   ═══════════════════════════════════════                       │
│                                                                  │
│   1. Usuário envia mensagem no WhatsApp                         │
│                    │                                             │
│                    ▼                                             │
│   2. Meta (Facebook) recebe                                      │
│                    │                                             │
│                    ▼                                             │
│   3. Meta "toca a campainha" do seu servidor                    │
│      POST https://seu-servidor.com/webhook                       │
│      Body: { "entry": [...], "messages": [...] }                │
│                    │                                             │
│                    ▼                                             │
│   4. Seu servidor abre a porta e processa                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Segurança: HMAC

```python
# Por que validar HMAC?
# Para garantir que a requisição veio REALMENTE do WhatsApp

def validate_signature(self, payload: bytes, signature: str) -> bool:
    """
    HMAC = Hash-based Message Authentication Code

    1. WhatsApp assina a mensagem com uma chave secreta
    2. Seu servidor recalcula a assinatura
    3. Se bater, é autêntico!
    """
    expected_hash = hmac.new(
        self._app_secret.encode(),  # Sua chave secreta
        payload,                     # Conteúdo da mensagem
        hashlib.sha256              # Algoritmo
    ).hexdigest()

    # Comparação segura (evita timing attacks)
    return hmac.compare_digest(computed, expected)
```

---

## FASE 7: Handler de Mensagens

### O que foi feito
Conectar todas as peças: Webhook → UseCase → WhatsApp Client.

### Fluxo Completo

```python
# src/presentation/whatsapp/handler.py

class MessageHandler:
    """Orquestra o processamento de mensagens."""

    async def handle(self, phone: str, text: str, message_id: str):
        """
        FLUXO COMPLETO:
        1. Cria DTO de entrada
        2. Executa UseCase
        3. Envia resposta via WhatsApp Client
        """

        # 1. Empacotar dados
        input_dto = IncomingMessageDTO(
            phone_number=phone,
            text=text,
            message_id=message_id
        )

        # 2. Processar (UseCase faz toda a lógica)
        response = await self._use_case.execute(input_dto)

        # 3. Enviar resposta
        async with WhatsAppClient() as client:
            await client.send_text_message(
                to=phone,
                text=response.text
            )

        # 4. Marcar como lida
        await client.mark_as_read(message_id)
```

---

## FASE 8: Testes

### O que foi feito
Testes unitários e de integração.

### Tipos de Testes

| Tipo | O que testa | Velocidade |
|------|-------------|------------|
| **Unitário** | Uma função isolada | Muito rápido |
| **Integração** | Várias partes juntas | Médio |
| **E2E** | Sistema completo | Lento |

### Exemplo: Teste Unitário

```python
# tests/unit/domain/entities/test_customer.py

import pytest
from src.domain.entities.customer import Customer


class TestCustomer:
    """Testes para a entidade Customer."""

    def test_create_customer_valid_phone(self):
        """Deve criar cliente com telefone válido."""
        customer = Customer(phone_number="5511999999999")

        assert customer.phone_number == "5511999999999"
        assert customer.id is not None

    def test_create_customer_cleans_phone(self):
        """Deve limpar caracteres do telefone."""
        customer = Customer(phone_number="+55 (11) 99999-9999")

        # Deve remover +, espaços, parênteses, hífen
        assert customer.phone_number == "5511999999999"

    def test_invalid_phone_raises_error(self):
        """Telefone inválido deve gerar erro."""
        with pytest.raises(ValueError):
            Customer(phone_number="123")  # Muito curto!
```

### Conceitos de Teste

#### 1. Fixtures

```python
@pytest.fixture
def mock_customer_repo():
    """Fixture = "Preparação" reutilizável."""
    return AsyncMock(spec=ICustomerRepository)

def test_algo(mock_customer_repo):  # Recebe automaticamente
    mock_customer_repo.find_by_phone.return_value = None
```

#### 2. Mocks

```python
# Mock = "Boneco de crash test"
# Simula comportamento sem usar o real

mock_repo = AsyncMock()
mock_repo.find_by_phone.return_value = Customer(phone="123")

# Quando chamar find_by_phone, retorna o Customer fake
```

---

## FASE 9: Docker

### O que foi feito
Containerização com Docker e docker-compose.

### Por que Docker?

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   PROBLEMA: "Na minha máquina funciona!"                        │
│   ═══════════════════════════════════════                       │
│                                                                  │
│   Desenvolvedor:  Python 3.12, PostgreSQL 16, Redis 7           │
│   Servidor:       Python 3.9, PostgreSQL 14, sem Redis          │
│                                                                  │
│   SOLUÇÃO: Docker                                               │
│   ════════════════                                              │
│                                                                  │
│   Docker empacota TUDO junto:                                   │
│   - Código                                                       │
│   - Dependências                                                 │
│   - Versões exatas                                              │
│   - Configurações                                                │
│                                                                  │
│   Roda IGUAL em qualquer lugar!                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### docker-compose.yml

```yaml
# Orquestra 3 containers

services:
  app:                    # Seu código
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis

  postgres:               # Banco de dados
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret

  redis:                  # Cache
    image: redis:7
```

### Comandos Docker

| Comando | O que faz |
|---------|-----------|
| `docker-compose up` | Sobe todos os containers |
| `docker-compose down` | Para todos |
| `docker-compose logs app` | Ver logs do app |
| `docker-compose exec app bash` | Entrar no container |

---

# PARTE 3: DEBUGGING

## 3.1 Erros Comuns e Soluções

### Erro: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'src'
```

**Causas possíveis:**
1. Ambiente virtual não está ativado
2. Dependências não instaladas
3. PYTHONPATH não configurado

**Soluções:**
```bash
# 1. Ativar ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Instalar dependências
uv pip install -e ".[dev]"

# 3. Verificar instalação
python -c "from src.config.settings import get_settings; print('OK')"
```

---

### Erro: Connection Refused (Banco)

```
sqlalchemy.exc.OperationalError: connection refused
```

**Causas:**
1. PostgreSQL não está rodando
2. URL do banco incorreta
3. Credenciais erradas

**Soluções:**
```bash
# 1. Verificar se PostgreSQL está rodando
docker-compose ps

# 2. Verificar .env
cat .env | grep DATABASE_URL

# 3. Testar conexão manual
docker-compose exec postgres psql -U user -d chatbot_db
```

---

### Erro: WhatsApp Webhook 403

```
HTTP 403 Forbidden
```

**Causas:**
1. Verify token não bate
2. Assinatura HMAC inválida
3. URL do webhook incorreta

**Soluções:**
1. Conferir `WHATSAPP_VERIFY_TOKEN` no .env
2. Conferir `WHATSAPP_WEBHOOK_SECRET` no .env
3. Verificar URL no painel Meta

---

## 3.2 Como Ler Stack Traces

```python
Traceback (most recent call last):
  File "src/main.py", line 45, in <module>      # ← Início
    app = create_app()
  File "src/main.py", line 30, in create_app
    settings = get_settings()
  File "src/config/settings.py", line 50, in get_settings
    return Settings()                            # ← Onde falhou
pydantic_settings.ValidationError:
  secret_key: Field required                     # ← O que faltou
```

**Leitura de baixo para cima:**
1. `secret_key: Field required` → Faltou configurar SECRET_KEY
2. `settings.py line 50` → Erro ao criar Settings
3. `main.py line 30` → Chamou get_settings()

---

## 3.3 Checklist de Troubleshooting

```
□ Ambiente virtual ativado?
□ Dependências instaladas?
□ .env existe e está configurado?
□ PostgreSQL rodando?
□ Redis rodando?
□ Migrations aplicadas?
□ Tokens WhatsApp configurados?
□ ngrok ativo (para testes)?
□ Webhook configurado no Meta?
```

---

# PARTE 4: DIAGRAMAS

## 4.1 Arquitetura Completa

```
┌─────────────────────────────────────────────────────────────────┐
│                         WHATSAPP                                 │
│                            📱                                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         META API                                 │
│                           ☁️                                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ POST /webhook
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SEU SERVIDOR                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    PRESENTATION                          │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │    │
│  │  │   FastAPI   │  │  Webhook    │  │    Handler      │  │    │
│  │  │   /docs     │  │  /webhook   │  │                 │  │    │
│  │  └─────────────┘  └──────┬──────┘  └────────┬────────┘  │    │
│  └───────────────────────────┼─────────────────┼───────────┘    │
│                              │                 │                 │
│  ┌───────────────────────────┼─────────────────┼───────────┐    │
│  │                    APPLICATION              │            │    │
│  │                              │                           │    │
│  │              ┌───────────────▼───────────────┐          │    │
│  │              │     HandleMessageUseCase      │          │    │
│  │              │                               │          │    │
│  │              │  1. Buscar/criar cliente      │          │    │
│  │              │  2. Buscar/criar sessão       │          │    │
│  │              │  3. Identificar intenção      │          │    │
│  │              │  4. Gerar resposta            │          │    │
│  │              └───────────────┬───────────────┘          │    │
│  └───────────────────────────────┼─────────────────────────┘    │
│                                  │                               │
│  ┌───────────────────────────────┼─────────────────────────┐    │
│  │                    DOMAIN     │                          │    │
│  │                               │                          │    │
│  │  ┌────────────┐  ┌────────────┼────────────┐            │    │
│  │  │  Entities  │  │     Interfaces          │            │    │
│  │  │  Customer  │  │  ICustomerRepository    │            │    │
│  │  │  Product   │  │  IProductRepository     │            │    │
│  │  │  Order     │  │  IOrderRepository       │            │    │
│  │  │  Session   │  │  ISessionRepository     │            │    │
│  │  └────────────┘  └────────────┬────────────┘            │    │
│  └───────────────────────────────┼─────────────────────────┘    │
│                                  │ implementa                    │
│  ┌───────────────────────────────┼─────────────────────────┐    │
│  │                INFRASTRUCTURE │                          │    │
│  │                               ▼                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │    │
│  │  │  PostgreSQL  │  │    Redis     │  │   WhatsApp   │   │    │
│  │  │  (SQLAlchemy)│  │   (Cache)    │  │   Client     │   │    │
│  │  └──────┬───────┘  └──────────────┘  └──────┬───────┘   │    │
│  └─────────┼────────────────────────────────────┼──────────┘    │
│            │                                    │                │
└────────────┼────────────────────────────────────┼────────────────┘
             │                                    │
             ▼                                    ▼
      ┌──────────────┐                    ┌──────────────┐
      │  PostgreSQL  │                    │   Meta API   │
      │     🐘       │                    │      ☁️       │
      └──────────────┘                    └──────────────┘
```

## 4.2 Ciclo de Vida da Sessão

```
┌─────────────────────────────────────────────────────────────────┐
│                    ESTADOS DA SESSÃO                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                         INITIAL                                  │
│                            │                                     │
│                   "Olá" ou "Menu"                               │
│                            │                                     │
│                            ▼                                     │
│                          MENU ◄──────────────────────────────┐  │
│                            │                                  │  │
│          ┌─────────────────┼─────────────────┐               │  │
│          │                 │                 │               │  │
│     "produtos"        "pedido"          "ajuda"         "voltar" │
│          │                 │                 │               │  │
│          ▼                 ▼                 ▼               │  │
│       PRODUCTS        ORDER_STATUS         FAQ ─────────────┘  │
│          │                 │                                    │
│          │         (digita número)                              │
│          │                 │                                    │
│          │                 ▼                                    │
│          │         TRACKING_RESULT                              │
│          │                                                      │
│     "atendente"                                                 │
│          │                                                      │
│          ▼                                                      │
│    HUMAN_TRANSFER                                               │
│          │                                                      │
│    (atendente assume)                                           │
│          │                                                      │
│          ▼                                                      │
│        CLOSED                                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

# FIM DO GUIA

**Próximos passos:**
1. Leia o `GUIA_TESTE_WHATSAPP.md` para testar
2. Faça a `PROVA_30_QUESTOES.md` para fixar
3. Confira as respostas no `GABARITO_PROVA.md`

---

**Desenvolvido com dedicação para seu aprendizado!** 🚀
