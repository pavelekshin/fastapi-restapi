# FastAPI RESTAPI Example Project

- well-structured easy to understand and scale-up project structure
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
- cookies based auth (http-only)
- salted password storage with `bcrypt`
- redis cache
- pydantic model
- FastAPI dependencies and background task
- and some other extras, like global custom exceptions, index naming convention, shortcut scripts for alembic, pydantic
  context, custom model, etc...

## Local Development

### First Build Only

1. `cp .env.example .env`
2. `docker network create app_weather`
3. `docker-compose up -d --build`

### Linters

Code formated with ruff

```shell
ruff --fix, ruff format
```

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

