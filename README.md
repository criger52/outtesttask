## Wallet service test task

REST API сервис для работы с кошельками пользователей, реализованный на асинхронном FastAPI с использованием clean architecture, Dishka (DI), SQLAlchemy async и PostgreSQL.

### Функциональность

- **Изменение баланса кошелька**
  - `POST /api/v1/wallets/{wallet_id}/operation`
  - Тело запроса:
    ```json
    {
      "operation_type": "DEPOSIT" | "WITHDRAW",
      "amount": 1000
    }
    ```
  - Ответ:
    ```json
    {
      "wallet_balance": 1000
    }
    ```
- **Получение баланса кошелька**
  - `GET /api/v1/wallets/{wallet_id}`
  - Ответ:
    ```json
    {
      "wallet_balance": 1000
    }
    ```

### Архитектура

- **domain**
  - `wallet/entities.py` — доменная сущность `Wallet` с инвариантами по балансу.
  - `wallet/exceptions.py` — доменные исключения (`WalletNotFoundError`, `InvalidAmountError`, `InsufficientFundsError`).
  - `wallet/interfaces.py` — абстракция `WalletRepository`.
- **application**
  - `wallet/use_cases.py` — `WalletService`, `OperationType`, `ChangeBalanceInput`.
- **infrastructure**
  - `db/models.py` — SQLAlchemy модель `WalletModel`.
  - `db/session.py` — асинхронная сессия и фабрика.
  - `db/repositories.py` — реализация `SqlAlchemyWalletRepository` с блокировкой строк (`SELECT ... FOR UPDATE`).
  - `di.py` — контейнер Dishka и провайдеры (`AsyncSession`, `WalletRepository`, `WalletService`).
- **presentation**
  - `presentation/api/rest/v1/schemas/` — pydantic-схемы (`wallet_balance.py`, `wallet_operation.py`).
  - `presentation/api/rest/v1/endpoints/` — эндпоинты (`get_wallet.py`, `change_wallet_balance.py`).
  - `presentation/api/rest/v1/routers.py` — сборка API v1.

Точка входа приложения: `src/main.py`, фабрика `create_app()` и объект `app` для ASGI-сервера.

### Запуск в Docker

Требуется Docker и docker-compose.

```bash
docker compose up --build
```

Сервис будет доступен по адресу `http://localhost:8000`, документация Swagger — по адресу `http://localhost:8000/docs`.

Перед первым запуском можно применить миграции Alembic:

```bash
docker compose run --rm app alembic upgrade head
```

### Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

uvicorn src.main:app --reload
```

По умолчанию приложение ожидает PostgreSQL по адресу `postgresql+asyncpg://wallet:wallet@db:5432/wallets` (см. `DATABASE_URL` в `infrastructure/db/session.py`). Для локального запуска можно переопределить переменную окружения:

```bash
export DATABASE_URL="postgresql+asyncpg://wallet:wallet@localhost:5432/wallets"
```

и применить миграции:

```bash
alembic upgrade head
```

### Тесты

Тесты лежат в каталоге `tests` и покрывают базовые сценарии работы API.

Запуск тестов:

```bash
pytest
```

### Линтинг

В проекте используется `ruff`:

```bash
ruff check .
```

