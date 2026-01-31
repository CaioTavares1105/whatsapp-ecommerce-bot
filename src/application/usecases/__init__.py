# ===========================================================
# src/application/usecases/__init__.py
# ===========================================================
"""
Casos de uso da aplicação.

Cada caso de uso representa UMA ação que o usuário pode fazer.
Segue o padrão: uma classe com um método execute().

Exemplo:
    class HandleMessageUseCase:
        def __init__(self, customer_repo, session_repo):
            self._customer_repo = customer_repo
            self._session_repo = session_repo
        
        async def execute(self, message_dto) -> ResponseDTO:
            # Lógica do caso de uso
            pass
"""
