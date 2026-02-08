# PROVA PRÁTICA: WhatsApp E-commerce Bot

## 30 Questões para Fixar o Conhecimento

**Tempo sugerido:** 60 minutos
**Pontuação:** 1 ponto por questão
**Aprovação:** 21 pontos (70%)

---

# INSTRUÇÕES

- Leia cada questão com atenção
- As questões práticas referenciam código real do projeto
- Anote suas respostas em uma folha separada
- Depois confira no arquivo `GABARITO_PROVA.md`

---

# SEÇÃO 1: PYTHON BÁSICO (5 questões)

---

## QUESTÃO 1: @dataclass

Analise o código abaixo:

```python
from dataclasses import dataclass, field
import uuid

@dataclass
class Product:
    name: str
    price: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
```

O que acontece quando você faz `p = Product("Camiseta", 49.90)`?

a) Erro, pois faltou passar o `id`
b) `p.id` será `None`
c) `p.id` terá um UUID único gerado automaticamente
d) `p.id` terá o valor `"uuid"`

---

## QUESTÃO 2: Type Hints

Qual é a forma correta de indicar que um atributo pode ser `str` OU `None`?

a) `name: str = None`
b) `name: str | None = None`
c) `name: Optional = None`
d) `name: (str, None) = None`

---

## QUESTÃO 3: field(default_factory)

Por que usamos `field(default_factory=list)` em vez de `itens: list = []`?

```python
@dataclass
class Carrinho:
    itens: list = field(default_factory=list)  # ✓
    # itens: list = []  # ✗
```

a) Porque `[]` não é uma lista válida
b) Para evitar que todas as instâncias compartilhem a mesma lista
c) Porque o Python exige essa sintaxe
d) Para economizar memória

---

## QUESTÃO 4: __post_init__

Quando o método `__post_init__` é executado?

```python
@dataclass
class Customer:
    phone: str

    def __post_init__(self):
        self.phone = self.phone.strip()
```

a) Antes do `__init__`
b) Depois do `__init__`, após os atributos serem definidos
c) Apenas quando chamado manualmente
d) Quando o objeto é destruído

---

## QUESTÃO 5: async/await

O que significa uma função ser `async`?

```python
async def buscar_cliente(phone: str) -> Customer:
    cliente = await repo.find_by_phone(phone)
    return cliente
```

a) A função roda em paralelo automaticamente
b) A função pode pausar e liberar recursos enquanto espera operações I/O
c) A função é mais rápida que funções normais
d) A função só pode ser chamada uma vez

---

# SEÇÃO 2: CLEAN ARCHITECTURE (5 questões)

---

## QUESTÃO 6: Camadas

Na Clean Architecture, qual é a ordem CORRETA das camadas, do mais interno ao mais externo?

a) Presentation → Application → Domain → Infrastructure
b) Domain → Application → Infrastructure → Presentation
c) Domain → Application → Presentation → Infrastructure
d) Infrastructure → Domain → Application → Presentation

---

## QUESTÃO 7: Regra de Dependência

Qual afirmação sobre dependências entre camadas está CORRETA?

a) Domain pode importar Infrastructure
b) Application pode importar Domain
c) Presentation pode importar diretamente Domain entities
d) Infrastructure não pode importar nada

---

## QUESTÃO 8: Responsabilidades

Qual camada é responsável por definir as REGRAS DE NEGÓCIO puras?

a) Presentation
b) Application
c) Domain
d) Infrastructure

---

## QUESTÃO 9: Onde fica o SQL?

Em qual camada ficam as implementações de acesso ao banco de dados (SQL)?

a) Domain
b) Application
c) Presentation
d) Infrastructure

---

## QUESTÃO 10: Por que separar?

Qual é o PRINCIPAL benefício de separar o código em camadas?

a) O código fica mais bonito
b) Permite trocar implementações sem afetar regras de negócio
c) Aumenta a performance
d) Reduz o número de arquivos

---

# SEÇÃO 3: PADRÕES DE PROJETO (5 questões)

---

## QUESTÃO 11: Repository Pattern

O que é uma Interface de Repositório (ICustomerRepository)?

```python
class ICustomerRepository(ABC):
    @abstractmethod
    async def find_by_phone(self, phone: str) -> Customer | None:
        ...
```

a) Uma classe que acessa o banco diretamente
b) Um contrato que define QUAIS métodos existem, sem implementar
c) Uma tabela do banco de dados
d) Um tipo de teste automatizado

---

## QUESTÃO 12: ABC

O que acontece se você tentar fazer `repo = ICustomerRepository()`?

a) Cria uma instância vazia
b) Erro: não pode instanciar classe abstrata
c) Cria com métodos padrão
d) Depende do Python version

---

## QUESTÃO 13: DTO

Qual é a função de um DTO (Data Transfer Object)?

```python
class IncomingMessageDTO(BaseModel):
    phone_number: str
    text: str
```

a) Armazenar dados no banco
b) Transportar dados entre camadas de forma estruturada
c) Validar regras de negócio
d) Executar queries SQL

---

## QUESTÃO 14: Use Case

Qual é a responsabilidade de um Use Case (HandleMessageUseCase)?

a) Armazenar dados
b) Renderizar interface do usuário
c) Orquestrar o fluxo de uma operação de negócio
d) Definir tabelas do banco

---

## QUESTÃO 15: Injeção de Dependência

No código abaixo, por que recebemos `repo` como parâmetro?

```python
class HandleMessageUseCase:
    def __init__(self, repo: ICustomerRepository):
        self._repo = repo
```

a) Porque é mais rápido
b) Para permitir trocar a implementação (ex: mock nos testes)
c) Porque Python exige
d) Para economizar memória

---

# SEÇÃO 4: SQLALCHEMY (5 questões)

---

## QUESTÃO 16: Mapped[tipo]

O que significa `Mapped[str]` no SQLAlchemy 2.0?

```python
class CustomerModel(Base):
    phone_number: Mapped[str] = mapped_column(String(15))
```

a) O campo será ignorado pelo ORM
b) Define o tipo Python e permite que SQLAlchemy mapeie para coluna SQL
c) O campo é opcional
d) O campo é uma chave estrangeira

---

## QUESTÃO 17: mapped_column

O que faz `unique=True` e `index=True`?

```python
phone_number: Mapped[str] = mapped_column(
    String(15),
    unique=True,
    index=True
)
```

a) `unique`: permite duplicatas; `index`: ordenação
b) `unique`: valor único na tabela; `index`: busca mais rápida
c) `unique`: não pode ser NULL; `index`: chave primária
d) `unique`: cria constraint; `index`: desabilita buscas

---

## QUESTÃO 18: relationship

O que representa o código abaixo?

```python
class CustomerModel(Base):
    orders: Mapped[list["OrderModel"]] = relationship(back_populates="customer")
```

a) Uma coluna chamada "orders"
b) Um relacionamento 1:N - um customer tem muitos orders
c) Uma chave primária composta
d) Uma tabela de junção

---

## QUESTÃO 19: Engine vs Session

Qual é a diferença entre Engine e Session no SQLAlchemy?

a) Engine é para leitura, Session é para escrita
b) Engine é a conexão geral, Session é uma "conversa" temporária com o banco
c) Engine é mais rápido, Session é mais seguro
d) Não há diferença, são sinônimos

---

## QUESTÃO 20: Async Session

Por que usamos `async with AsyncSessionFactory() as session`?

```python
async def get_db_session():
    async with AsyncSessionFactory() as session:
        yield session
```

a) Para que a sessão seja fechada automaticamente ao final
b) Para criar múltiplas sessões
c) Para desabilitar transações
d) Para ignorar erros

---

# SEÇÃO 5: FASTAPI (5 questões)

---

## QUESTÃO 21: APIRouter

O que faz o código abaixo?

```python
router = APIRouter(prefix="/webhook", tags=["WhatsApp"])

@router.get("/")
async def verify_webhook():
    return {"status": "ok"}
```

a) Cria um endpoint em `/webhook/` que retorna `{"status": "ok"}`
b) Cria uma tabela chamada "webhook"
c) Define uma variável de ambiente
d) Envia uma mensagem WhatsApp

---

## QUESTÃO 22: Depends

O que faz `Depends()` no FastAPI?

```python
@router.post("/webhook")
async def receive(
    session: AsyncSession = Depends(get_db_session)
):
    ...
```

a) Define um valor padrão
b) Injeta uma dependência automaticamente (injeção de dependência)
c) Valida o tipo do parâmetro
d) Cria uma nova rota

---

## QUESTÃO 23: BackgroundTasks

O que acontece quando usamos BackgroundTasks?

```python
@router.post("/webhook")
async def receive(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_message, data)
    return {"status": "received"}
```

a) A resposta só é enviada após `process_message` terminar
b) A resposta é enviada imediatamente e `process_message` roda depois
c) `process_message` nunca é executado
d) Cria uma nova thread bloqueante

---

## QUESTÃO 24: Response Status

Qual status HTTP indica sucesso em uma requisição POST?

a) 100
b) 200
c) 404
d) 500

---

## QUESTÃO 25: Health Check

Para que serve um endpoint `/health`?

```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

a) Para verificar se a API está respondendo (monitoramento)
b) Para retornar dados médicos
c) Para autenticar usuários
d) Para salvar logs

---

# SEÇÃO 6: WHATSAPP API E DEBUGGING (5 questões)

---

## QUESTÃO 26: Webhook

O que é um Webhook no contexto do WhatsApp?

a) Um tipo de mensagem com imagem
b) Uma URL que o WhatsApp chama quando há novas mensagens
c) Um número de telefone virtual
d) Um tipo de criptografia

---

## QUESTÃO 27: HMAC

Por que validamos a assinatura HMAC das requisições?

```python
def validate_signature(self, payload: bytes, signature: str) -> bool:
    expected = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, expected)
```

a) Para acelerar o processamento
b) Para garantir que a requisição veio realmente do WhatsApp
c) Para comprimir os dados
d) Para criptografar a mensagem

---

## QUESTÃO 28: Verify Token

Para que serve o "Verify Token" na configuração do Webhook?

a) Para autenticar o usuário do WhatsApp
b) Para confirmar que VOCÊ é o dono do servidor ao configurar
c) Para enviar mensagens
d) Para acessar o painel Meta

---

## QUESTÃO 29: ngrok

Por que usamos ngrok durante o desenvolvimento?

a) Para deixar o código mais rápido
b) Para expor localhost para a internet (túnel público)
c) Para compilar o Python
d) Para instalar dependências

---

## QUESTÃO 30: Debug - Mensagem não chega

Você envia "Olá" no WhatsApp mas não recebe resposta. O log do servidor mostra:

```
POST /webhook - 200 OK
Processing message from 5511999999999
ERROR: MockProductRepository has no attribute 'find_all'
```

Qual é a causa mais provável?

a) O token do WhatsApp expirou
b) O banco de dados está offline
c) Estão sendo usados repositórios Mock em vez de implementações reais
d) O ngrok parou de funcionar

---

# FIM DA PROVA

---

## Instruções para Correção

1. Anote suas respostas (1-30)
2. Abra o arquivo `GABARITO_PROVA.md`
3. Compare suas respostas
4. Calcule sua pontuação

---

## Escala de Aproveitamento

| Pontos | Classificação |
|--------|---------------|
| 27-30 | Excelente! Pronto para produção |
| 24-26 | Muito bom! Revise pontos fracos |
| 21-23 | Aprovado! Estude mais alguns tópicos |
| 18-20 | Quase lá! Revise as seções com mais erros |
| < 18 | Releia o GUIA_COMPLETO_PROJETO.md |

---

**Boa prova!** 📝
