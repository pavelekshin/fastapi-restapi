# FastAPI RESTAPI Example Project

- well-structured easy to understand and scale-up project structure


```bash
.
├── Dockerfile
├── README.md
├── alembic
├── alembic.ini
├── docker-compose.yml
├── logging.ini
├── requirements.txt
├── ruff.toml
├── .env
├── scripts                       - scripts for container
│   ├── downgrade
│   ├── makemigrations
│   ├── create-admin
│   ├── migrate
│   └── start-dev.sh
└── src                           - global configuration
    ├── __init__.py
    ├── auth                      - auth modul 
    │   ├── __init__.py
    │   ├── config.py
    │   ├── constants.py
    │   ├── dependencies.py       - auth dependencies
    │   ├── exceptions.py         - auth exceptions
    │   ├── jwt.py                - jwt configuration
    │   ├── router.py         
    │   ├── schemas.py            - pydantic schema
    │   ├── security.py           - security stuff
    │   ├── service.py            - service logic
    │   └── utils.py              - stuff
    ├── config                      
    │   └── config.py
    ├── constants.py              - global constants
    ├── database.py               - db settings
    ├── exception_handlers.py     - global exception_handlers
    ├── exceptions.py             - global exceptions
    ├── main.py
    ├── tools                     - tools for create auth Admin
    │   └── create_auth_admin.py                       
    ├── models
    │   └── models.py             - global pydantic model
    ├── redis.py                  - global redis configuration
    ├── settings.py               - global settings 
    └── weather_service           - weather service modul
        ├── __init__.py
        ├── client.py             - weather client
        ├── constants.py          - weather constants
        ├── exceptions.py         - weather exceptions
        ├── helper.py             - helper func
        ├── router.py             - weather routers
        └── schemas.py            - pydantic schema

```
- async IO operations
- easy local development
    - Dockerfile optimized for small size and fast builds with a non-root user
    - Docker-compose for easy deployment
    - environment with configured Postgres and Redis
- SQLAlchemy with slightly configured `alembic`
    - async SQLAlchemy engine
    - migrations set in easy to understand format (`YYYY-MM-DD_HHmm_rev_slug`)
- SQLAlchemy Core query
- OAuth2 JWT with refresh token
- cookies based updated token (http-only)
- salted password storage with `bcrypt`
- redis cache
- pydantic model
- linters / format with ruff
- FastAPI dependencies and background task
- and some other extras, like global custom exceptions, index naming convention, shortcut scripts for alembic, pydantic
  context, custom model, etc...

## Local Development

### First Build Only

1. `cp .env.example .env`
2. `docker network create app_weather`
3. `docker-compose up -d --build`

### Migrations

- Create an automatic migration from changes in `src/database.py`

```shell
docker compose exec app makemigrations *migration_name*
```

- Run migrations

```shell
docker compose exec app migrate
```

- Downgrade migrations

```shell
docker compose exec app downgrade -1  # or -2 or base or hash of the migration
```

- Create user with Admin role

```shell
docker compose exec app create-admin -e Abc@example.com -p StrongPa$$w0rd  # Create user with Admin role
```

### Swagger UI

```shell
http://localhost:15000/docs
```
