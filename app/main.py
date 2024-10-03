from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.database.base import Base
from app.database.session import engine

app = FastAPI(
    title="Wwon Application",
    description="""API REST em Python para classificar automaticamente as 
                    avaliações de clientes sobre o serviço/produto/suporte 
                    (exemplos em anexo) de uma empresa em Positiva, Negativa ou Neutra.""",
    version="0.1.0",
)

# Criar tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Incluir rotas
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
