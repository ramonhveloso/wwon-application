# BACKEND

## Requisitos

- [Python 3.x](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://www.docker.com/get-started)

## Configuração do Ambiente

1. **Crie uma chave SSH e clone o repositório:**

   `git clone git@github.com:ramonhveloso/wwon-application.git`

2. **Instale as dependências usando Poetry:**

   `poetry install`

3. **Configuração do banco de dados:**

   Para executar o PostgreSQL usando Docker, execute o seguinte comando:

   `docker run -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=postgre -e POSTGRES_DB=desenvolvimento -d --name=wwon_local postgres:14.10`

4. **Configuração do Alembic:**

   - Configure o arquivo `alembic.ini` para apontar para o seu banco de dados PostgreSQL. Certifique-se de que a URL do banco de dados esteja correta.

   `sqlalchemy.url = postgresql://admin:postgre@localhost:5432/desenvolvimento`

5. **Executar as migrações do Alembic:**

   Para criar as tabelas no banco de dados, execute o seguinte comando:

   `alembic upgrade head`

## Executando a Aplicação

`uvicorn app.main:app --reload`

## Parar o Container do PostgreSQL

Para parar o container do PostgreSQL, use:

`docker stop wwon application_local`

## Remover o Container do PostgreSQL

Para remover o container, use:

`docker rm wwon application_local`

## Contribuição

Se você deseja contribuir com o projeto, fique à vontade para fazer um fork do repositório e enviar um pull request.

## Licença

Este projeto é licenciado sob a Licença Privada. Todos os direitos reservados. O uso e a distribuição do código são restritos. Para mais informações, entre em contato. 
