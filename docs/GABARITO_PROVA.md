# GABARITO DA PROVA

## 30 Questões com Respostas e Explicações

---

# TABELA DE RESPOSTAS RÁPIDAS

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|----|----|----|----|----|----|----|----|----|-----|
| c  | b  | b  | b  | b  | c  | b  | c  | d  | b   |

| Q11 | Q12 | Q13 | Q14 | Q15 | Q16 | Q17 | Q18 | Q19 | Q20 |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| b   | b   | b   | c   | b   | b   | b   | b   | b   | a   |

| Q21 | Q22 | Q23 | Q24 | Q25 | Q26 | Q27 | Q28 | Q29 | Q30 |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| a   | b   | b   | b   | a   | b   | b   | b   | b   | c   |

---

# EXPLICAÇÕES DETALHADAS

---

## SEÇÃO 1: PYTHON BÁSICO

---

### QUESTÃO 1: c

**Resposta:** `p.id` terá um UUID único gerado automaticamente

**Explicação:**
`field(default_factory=lambda: str(uuid.uuid4()))` gera um UUID novo CADA VEZ que um Product é criado. O `default_factory` é uma função que é chamada para gerar o valor padrão.

**Referência:** `src/domain/entities/product.py` linha 23

**Conceito:** Default factory em dataclasses

---

### QUESTÃO 2: b

**Resposta:** `name: str | None = None`

**Explicação:**
Desde Python 3.10, podemos usar `tipo1 | tipo2` para indicar união de tipos. Isso significa "pode ser str OU None". É equivalente a `Optional[str]` das versões anteriores.

**Referência:** `src/domain/entities/customer.py` linha 22

**Conceito:** Type hints com Union types

---

### QUESTÃO 3: b

**Resposta:** Para evitar que todas as instâncias compartilhem a mesma lista

**Explicação:**
Em Python, valores mutáveis como `[]` são criados UMA vez e compartilhados. Se usarmos `itens: list = []`, TODOS os carrinhos teriam a MESMA lista! Com `default_factory=list`, cada instância recebe uma lista NOVA.

**Referência:** Conceito Python, não no código

**Conceito:** Mutable default argument pitfall

---

### QUESTÃO 4: b

**Resposta:** Depois do `__init__`, após os atributos serem definidos

**Explicação:**
`__post_init__` é executado APÓS o `__init__` gerado pelo `@dataclass`. Nesse ponto, todos os atributos já existem. É o lugar ideal para validações e transformações.

**Referência:** `src/domain/entities/customer.py` linha 31

**Conceito:** Dataclass lifecycle

---

### QUESTÃO 5: b

**Resposta:** A função pode pausar e liberar recursos enquanto espera operações I/O

**Explicação:**
`async` não é paralelismo verdadeiro. É cooperativo: quando a função encontra `await`, ela PAUSA e deixa outras tarefas rodarem. Isso é eficiente para I/O (banco, rede) porque não bloqueia a thread.

**Referência:** `src/infrastructure/database/connection.py`

**Conceito:** Async/await e event loop

---

## SEÇÃO 2: CLEAN ARCHITECTURE

---

### QUESTÃO 6: c

**Resposta:** Domain → Application → Presentation → Infrastructure

**Explicação:**
Na verdade, a ordem visual pode variar, mas a regra é:
- **Domain** está no CENTRO (mais interno)
- **Infrastructure** fica FORA mas APONTA para dentro

A ordem de "dentro para fora" é: Domain → Application → (Presentation e Infrastructure são ambas externas, com Infrastructure implementando interfaces do Domain)

**Referência:** `CLAUDE.md` seção "Arquitetura do Sistema"

**Conceito:** Clean Architecture layers

---

### QUESTÃO 7: b

**Resposta:** Application pode importar Domain

**Explicação:**
Regra de dependência: camadas externas podem importar internas.
- Application (externa) pode importar Domain (interna) ✓
- Domain NÃO importa ninguém (é o núcleo)
- Infrastructure implementa interfaces do Domain

**Referência:** `CLAUDE.md` seção "Clean Architecture"

**Conceito:** Dependency Rule

---

### QUESTÃO 8: c

**Resposta:** Domain

**Explicação:**
A camada Domain contém:
- Entidades (Customer, Product, Order)
- Regras de negócio ("telefone deve ter 10-15 dígitos")
- Interfaces de repositório (contratos)

É a camada mais "pura" - não sabe nada de banco, HTTP, etc.

**Referência:** `src/domain/entities/`

**Conceito:** Domain Layer responsibility

---

### QUESTÃO 9: d

**Resposta:** Infrastructure

**Explicação:**
Infrastructure é a camada de "detalhes técnicos":
- SQLAlchemy (ORM)
- PostgreSQL (banco)
- Redis (cache)
- WhatsApp Client (API externa)

Ela IMPLEMENTA as interfaces definidas no Domain.

**Referência:** `src/infrastructure/database/repositories/`

**Conceito:** Infrastructure Layer responsibility

---

### QUESTÃO 10: b

**Resposta:** Permite trocar implementações sem afetar regras de negócio

**Explicação:**
Se amanhã você quiser trocar PostgreSQL por MongoDB:
- Sem camadas: reescreve TUDO
- Com camadas: cria nova implementação de `ICustomerRepository`, Domain não muda!

**Referência:** Conceito arquitetural

**Conceito:** Separation of Concerns

---

## SEÇÃO 3: PADRÕES DE PROJETO

---

### QUESTÃO 11: b

**Resposta:** Um contrato que define QUAIS métodos existem, sem implementar

**Explicação:**
Interface = "Tomada elétrica". Define o formato (quais métodos), não a implementação. Qualquer classe que "encaixe" (implemente os métodos) funciona.

**Referência:** `src/domain/repositories/customer_repository.py`

**Conceito:** Interface / Abstract Base Class

---

### QUESTÃO 12: b

**Resposta:** Erro: não pode instanciar classe abstrata

**Explicação:**
Classes que herdam de `ABC` e têm métodos `@abstractmethod` NÃO podem ser instanciadas. Você DEVE criar uma classe filha que implementa todos os métodos abstratos.

**Referência:** `src/domain/repositories/customer_repository.py`

**Conceito:** Abstract Base Class

---

### QUESTÃO 13: b

**Resposta:** Transportar dados entre camadas de forma estruturada

**Explicação:**
DTO = "Envelope". Leva só os dados necessários de um lugar para outro. Entidade Customer tem 10 campos; DTO de resposta pode ter só 2.

**Referência:** `src/application/dtos/message_dto.py`

**Conceito:** Data Transfer Object pattern

---

### QUESTÃO 14: c

**Resposta:** Orquestrar o fluxo de uma operação de negócio

**Explicação:**
Use Case = "Maestro". Não toca instrumentos (não acessa banco, não envia HTTP). Ele COORDENA quem faz o quê, na ordem certa.

**Referência:** `src/application/usecases/handle_message.py`

**Conceito:** Use Case / Interactor pattern

---

### QUESTÃO 15: b

**Resposta:** Para permitir trocar a implementação (ex: mock nos testes)

**Explicação:**
Injeção de Dependência: receber de fora em vez de criar dentro.
- Em produção: passa SQLAlchemyCustomerRepository
- Em testes: passa MockCustomerRepository

O UseCase não sabe (nem se importa) qual é!

**Referência:** `src/application/usecases/handle_message.py` linha 30

**Conceito:** Dependency Injection

---

## SEÇÃO 4: SQLALCHEMY

---

### QUESTÃO 16: b

**Resposta:** Define o tipo Python e permite que SQLAlchemy mapeie para coluna SQL

**Explicação:**
`Mapped[str]` indica:
- Para Python: é uma string
- Para SQLAlchemy: mapeie para uma coluna VARCHAR

É a nova sintaxe do SQLAlchemy 2.0 com type hints.

**Referência:** `src/infrastructure/database/models.py` linha 25

**Conceito:** SQLAlchemy 2.0 Mapped types

---

### QUESTÃO 17: b

**Resposta:** `unique`: valor único na tabela; `index`: busca mais rápida

**Explicação:**
- `unique=True`: não permite dois clientes com mesmo telefone
- `index=True`: cria índice no banco para buscas rápidas

**Referência:** `src/infrastructure/database/models.py` linha 27

**Conceito:** Database constraints and indexes

---

### QUESTÃO 18: b

**Resposta:** Um relacionamento 1:N - um customer tem muitos orders

**Explicação:**
`Mapped[list["OrderModel"]]` = lista de orders
`back_populates="customer"` = o outro lado do relacionamento

Isso não cria coluna! É um relacionamento ORM.

**Referência:** `src/infrastructure/database/models.py` linha 40

**Conceito:** SQLAlchemy relationships

---

### QUESTÃO 19: b

**Resposta:** Engine é a conexão geral, Session é uma "conversa" temporária com o banco

**Explicação:**
- **Engine** = Restaurante (existe sempre)
- **Session** = Mesa onde você senta, faz pedidos, paga e vai embora

Engine é criada UMA vez. Sessions são criadas por request.

**Referência:** `src/infrastructure/database/connection.py`

**Conceito:** SQLAlchemy Engine vs Session

---

### QUESTÃO 20: a

**Resposta:** Para que a sessão seja fechada automaticamente ao final

**Explicação:**
`async with` é um context manager assíncrono. Garante que:
1. A sessão é criada ao entrar
2. A sessão é fechada (commit/rollback) ao sair
3. Recursos são liberados mesmo se der erro

**Referência:** `src/infrastructure/database/connection.py` linha 45

**Conceito:** Async context managers

---

## SEÇÃO 5: FASTAPI

---

### QUESTÃO 21: a

**Resposta:** Cria um endpoint em `/webhook/` que retorna `{"status": "ok"}`

**Explicação:**
- `APIRouter(prefix="/webhook")`: todos os endpoints deste router terão `/webhook` no início
- `@router.get("/")`: GET em `/webhook/`
- Retorna o dict, FastAPI converte para JSON

**Referência:** `src/presentation/api/routes/webhook.py`

**Conceito:** FastAPI routing

---

### QUESTÃO 22: b

**Resposta:** Injeta uma dependência automaticamente (injeção de dependência)

**Explicação:**
`Depends(get_db_session)` faz o FastAPI:
1. Chamar `get_db_session()` antes do endpoint
2. Passar o resultado como parâmetro
3. Lidar com cleanup depois

**Referência:** `src/presentation/api/dependencies.py`

**Conceito:** FastAPI Dependency Injection

---

### QUESTÃO 23: b

**Resposta:** A resposta é enviada imediatamente e `process_message` roda depois

**Explicação:**
BackgroundTasks permite:
1. Responder rápido (200 OK)
2. Processar devagar depois

Isso é essencial para webhooks: WhatsApp espera resposta em < 5 segundos!

**Referência:** `src/presentation/api/routes/webhook.py`

**Conceito:** FastAPI Background Tasks

---

### QUESTÃO 24: b

**Resposta:** 200

**Explicação:**
Códigos HTTP:
- 1xx: Informativo
- 2xx: Sucesso (200 OK, 201 Created)
- 3xx: Redirecionamento
- 4xx: Erro do cliente (404 Not Found)
- 5xx: Erro do servidor (500 Internal Error)

**Referência:** Conceito HTTP

**Conceito:** HTTP Status Codes

---

### QUESTÃO 25: a

**Resposta:** Para verificar se a API está respondendo (monitoramento)

**Explicação:**
Health check é usado por:
- Docker (healthcheck)
- Kubernetes (liveness/readiness probes)
- Ferramentas de monitoramento

Se `/health` não responde, algo está errado!

**Referência:** `src/main.py`

**Conceito:** Health Check pattern

---

## SEÇÃO 6: WHATSAPP API E DEBUGGING

---

### QUESTÃO 26: b

**Resposta:** Uma URL que o WhatsApp chama quando há novas mensagens

**Explicação:**
Webhook = "campainha inversa". Em vez de você perguntar "tem mensagem?", o WhatsApp AVISA você quando chega algo, fazendo um POST na sua URL.

**Referência:** `src/infrastructure/whatsapp/webhook.py`

**Conceito:** Webhook pattern

---

### QUESTÃO 27: b

**Resposta:** Para garantir que a requisição veio realmente do WhatsApp

**Explicação:**
Qualquer um pode fazer POST no seu servidor. HMAC garante:
1. WhatsApp assina a mensagem com chave secreta
2. Você verifica a assinatura
3. Se bater, é autêntico!

**Referência:** `src/infrastructure/whatsapp/webhook.py` linha 131

**Conceito:** HMAC authentication

---

### QUESTÃO 28: b

**Resposta:** Para confirmar que VOCÊ é o dono do servidor ao configurar

**Explicação:**
Ao configurar webhook, Meta faz um GET com o verify_token. Se você retornar o challenge correto, prova que controla o servidor.

**Referência:** `src/infrastructure/whatsapp/webhook.py`

**Conceito:** Webhook verification

---

### QUESTÃO 29: b

**Resposta:** Para expor localhost para a internet (túnel público)

**Explicação:**
Seu computador está "escondido" atrás do roteador. ngrok cria um túnel:
- `https://abc123.ngrok.io` → `localhost:8000`

Assim o WhatsApp consegue enviar requisições para você.

**Referência:** `docs/GUIA_TESTE_WHATSAPP.md`

**Conceito:** Tunneling / ngrok

---

### QUESTÃO 30: c

**Resposta:** Estão sendo usados repositórios Mock em vez de implementações reais

**Explicação:**
O erro `MockProductRepository has no attribute 'find_all'` indica:
1. O código está usando mocks de teste
2. Os mocks não têm todos os métodos
3. Precisa usar repositórios SQLAlchemy reais

**Referência:** `src/presentation/api/dependencies.py` (problema identificado na auditoria)

**Conceito:** Debugging / Mock vs Real implementation

---

# RESUMO POR SEÇÃO

| Seção | Pontos Possíveis | Sua Pontuação |
|-------|------------------|---------------|
| Python Básico | 5 | ___ |
| Clean Architecture | 5 | ___ |
| Padrões de Projeto | 5 | ___ |
| SQLAlchemy | 5 | ___ |
| FastAPI | 5 | ___ |
| WhatsApp/Debug | 5 | ___ |
| **TOTAL** | **30** | **___** |

---

# ANÁLISE DE ERROS

Se você errou várias questões de uma seção, revise:

| Seção | Material de Estudo |
|-------|-------------------|
| Python Básico | `GUIA_COMPLETO_PROJETO.md` Parte 1 |
| Clean Architecture | `GUIA_COMPLETO_PROJETO.md` Seção 1.3 |
| Padrões de Projeto | `GUIA_COMPLETO_PROJETO.md` Fases 3-4 |
| SQLAlchemy | `GUIA_COMPLETO_PROJETO.md` Fase 5 |
| FastAPI | `GUIA_COMPLETO_PROJETO.md` Fases 7 |
| WhatsApp/Debug | `GUIA_TESTE_WHATSAPP.md` |

---

# PRÓXIMOS PASSOS

Se você acertou **21+ questões**: Parabéns! Você está pronto para corrigir os problemas críticos e testar o chatbot.

Se você acertou **menos de 21**: Releia o material e refaça a prova em 24 horas.

---

**Bons estudos!** 📚
