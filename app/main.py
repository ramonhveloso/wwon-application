from fastapi import FastAPI

from app.api.v1.router import router as api_router
from app.database.base import Base
from app.database.session import engine

app = FastAPI(
    title="Boilerplate padrão back-end",
    description="""Este boilerplate oferece uma estrutura inicial otimizada para 
                    o desenvolvimento de APIs back-end robustas e escaláveis. 
                    Com foco em boas práticas de arquitetura, inclui configurações 
                    essenciais para autenticação, controle de erros, 
                    testes automatizados. 
                    Ideal para acelerar o desenvolvimento de projetos com FastAPI 
                    e facilmente adaptável a diferentes contextos de aplicação.""",
    version="0.1.0",
)

# Criar tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Incluir rotas
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
