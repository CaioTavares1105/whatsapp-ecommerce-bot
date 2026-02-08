# ===========================================================
# src/config/settings.py - Configurações da Aplicação
# ===========================================================
# Este módulo carrega as variáveis de ambiente do arquivo .env
# e as disponibiliza como atributos tipados.
#
# USA: Pydantic Settings (https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
#
# POR QUE USAR PYDANTIC SETTINGS?
# 1. Carrega .env automaticamente
# 2. Validação de tipos (string, int, bool)
# 3. Valores padrão
# 4. Documentação via type hints
# ===========================================================
"""
Configurações da aplicação usando Pydantic Settings.

Uso:
    from src.config.settings import get_settings
    
    settings = get_settings()
    print(settings.app_name)      # "whatsapp-ecommerce-bot"
    print(settings.debug)         # True (em desenvolvimento)
    print(settings.database_url)  # "postgresql+asyncpg://..."
"""

# functools.lru_cache - Decorator para cachear resultado de função
# Assim a função get_settings() só lê o .env UMA vez
from functools import lru_cache

# Pydantic Settings - Configuração baseada em variáveis de ambiente
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Cada atributo corresponde a uma variável de ambiente.
    O nome do atributo (em UPPERCASE) = nome da variável.
    
    Exemplo:
        app_name -> APP_NAME no .env
        database_url -> DATABASE_URL no .env
    
    Attributes:
        app_name: Nome da aplicação
        app_env: Ambiente (development, staging, production)
        debug: Modo debug ativado
        secret_key: Chave secreta para JWT e criptografia
        database_url: URL de conexão com PostgreSQL
        redis_url: URL de conexão com Redis
        whatsapp_*: Configurações da API do WhatsApp
        api_host: Host onde a API vai rodar
        api_port: Porta da API
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR)
    """
    
    # ===== CONFIGURAÇÃO DO PYDANTIC =====
    # Diz ao Pydantic onde encontrar as variáveis
    model_config = SettingsConfigDict(
        # Arquivo .env na raiz do projeto
        env_file=".env",
        
        # Encoding do arquivo (importante para acentos)
        env_file_encoding="utf-8",
        
        # Não diferencia maiúsculas/minúsculas
        # APP_NAME = app_name = App_Name
        case_sensitive=False,
        
        # Ignora variáveis extras no .env
        extra="ignore",
    )
    
    # ===== CONFIGURAÇÕES DA APLICAÇÃO =====
    # Valor após : é o DEFAULT se não existir no .env
    
    # Nome da aplicação (usado em logs e headers)
    app_name: str = "whatsapp-ecommerce-bot"
    
    # Ambiente de execução
    app_env: str = "development"
    
    # Modo debug (logs detalhados, erros expostos)
    # NUNCA use True em produção!
    debug: bool = False
    
    # Chave secreta (OBRIGATÓRIA - sem valor padrão)
    # Se não existir no .env, dá erro ao iniciar
    secret_key: str
    
    # ===== BANCO DE DADOS =====
    # URL de conexão PostgreSQL (OBRIGATÓRIA)
    database_url: str
    
    # ===== CACHE REDIS =====
    # URL de conexão Redis (opcional, tem valor padrão)
    redis_url: str = "redis://localhost:6379/0"
    
    # ===== WHATSAPP CLOUD API =====
    # Todas opcionais (str | None = pode ser None)
    whatsapp_api_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    whatsapp_verify_token: str | None = None
    whatsapp_webhook_secret: str | None = None
    
    # ===== CONFIGURAÇÃO DA API =====
    # Host (0.0.0.0 = aceita conexões de qualquer IP)
    api_host: str = "0.0.0.0"
    
    # Porta (8000 é padrão para APIs Python)
    api_port: int = 8000
    
    # ===== LOGGING =====
    log_level: str = "INFO"
    
    # ===== PROPRIEDADES COMPUTADAS =====
    # @property transforma método em atributo
    
    @property
    def is_production(self) -> bool:
        """
        Verifica se está em ambiente de produção.
        
        Returns:
            True se app_env == "production"
        """
        return self.app_env == "production"
    
    @property
    def is_development(self) -> bool:
        """
        Verifica se está em ambiente de desenvolvimento.
        
        Returns:
            True se app_env == "development"
        """
        return self.app_env == "development"
    
    # Propriedades de compatibilidade para WhatsApp
    @property
    def whatsapp_token(self) -> str:
        """Alias para whatsapp_api_token."""
        return self.whatsapp_api_token or ""
    
    @property
    def whatsapp_app_secret(self) -> str:
        """
        Alias para whatsapp_webhook_secret.

        SEGURANCA: Retorna string vazia se nao configurado,
        mas o webhook.py deve validar se esta vazio em producao!
        """
        return self.whatsapp_webhook_secret or ""

    def validate_security(self) -> list[str]:
        """
        Valida configuracoes de seguranca.

        Returns:
            Lista de problemas encontrados (vazia se OK)
        """
        issues = []

        if self.is_production:
            if self.debug:
                issues.append("CRITICAL: DEBUG=true em producao!")

            if not self.whatsapp_webhook_secret:
                issues.append("CRITICAL: WHATSAPP_WEBHOOK_SECRET vazio em producao!")

            if not self.secret_key or len(self.secret_key) < 32:
                issues.append("CRITICAL: SECRET_KEY muito curta (minimo 32 chars)!")

            if "localhost" in self.database_url:
                issues.append("WARNING: DATABASE_URL aponta para localhost em producao!")

        return issues


# ===== FUNÇÃO PARA OBTER CONFIGURAÇÕES =====

@lru_cache  # Cacheia o resultado (singleton)
def get_settings() -> Settings:
    """
    Retorna instância cacheada das configurações.
    
    Usar @lru_cache significa que:
    1. Na primeira chamada: cria objeto Settings (lê .env)
    2. Nas próximas chamadas: retorna o mesmo objeto
    
    Isso é importante porque:
    - Não relê o arquivo .env a cada chamada
    - Garante que todas as partes do código usam as mesmas configurações
    - É um padrão Singleton (uma única instância)
    
    Returns:
        Settings: Objeto com todas as configurações
        
    Raises:
        ValidationError: Se variáveis obrigatórias não existirem
        
    Example:
        >>> settings = get_settings()
        >>> print(settings.app_name)
        whatsapp-ecommerce-bot
    """
    return Settings()
