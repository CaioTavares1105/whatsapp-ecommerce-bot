# ===========================================================
# Dockerfile - Imagem Docker do WhatsApp Chatbot
# ===========================================================
# Multi-stage build para imagem otimizada.
#
# ESTÁGIOS:
# 1. builder: Instala dependências
# 2. runtime: Imagem final mínima
#
# COMO USAR:
# docker build -t whatsapp-bot .
# docker run -p 8000:8000 whatsapp-bot
# ===========================================================

# ===========================================================
# ESTÁGIO 1: BUILDER
# ===========================================================
# Instala dependências e prepara o ambiente

FROM python:3.12-slim AS builder

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema para compilação
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências
COPY pyproject.toml ./

# Instala as dependências no diretório /app/.venv
RUN python -m venv /app/.venv && \
    /app/.venv/bin/pip install --upgrade pip && \
    /app/.venv/bin/pip install .


# ===========================================================
# ESTÁGIO 2: RUNTIME
# ===========================================================
# Imagem final otimizada para produção

FROM python:3.12-slim AS runtime

# Labels para documentação
LABEL maintainer="WhatsApp E-commerce Bot" \
      version="0.1.0" \
      description="Chatbot WhatsApp para E-commerce"

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Diretório de trabalho
WORKDIR /app

# Instala dependências de runtime (libpq para PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia o virtualenv do estágio builder
COPY --from=builder /app/.venv /app/.venv

# Adiciona venv ao PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copia o código da aplicação
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Cria usuário não-root para segurança
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expõe a porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Comando para iniciar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
