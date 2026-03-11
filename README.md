# to-do-list-user-backend

Микросервис управления пользователями для приложения To-Do List. Отвечает за регистрацию, аутентификацию и управление профилем пользователя. Аутентификация построена на базе **Keycloak** (OAuth2 / JWT), хранилище данных — **PostgreSQL**. Сервис реализован на **FastAPI** с полностью асинхронным стеком и следует принципам **Domain-Driven Design (DDD)**.

---

## Оглавление

- [Что делает сервис](#что-делает-сервис)
- [Архитектура](#архитектура)
- [Технологический стек](#технологический-стек)
- [Требования](#требования)
- [Быстрый старт (Docker Compose)](#быстрый-старт-docker-compose)
- [Локальная разработка](#локальная-разработка)
- [Переменные окружения](#переменные-окружения)
- [Миграции базы данных](#миграции-базы-данных)
- [API Reference](#api-reference)
- [Тестирование](#тестирование)
- [Структура проекта](#структура-проекта)

---

## Что делает сервис

- **Регистрация пользователя** — создаёт пользователя одновременно в Keycloak и в локальной БД PostgreSQL.
- **Аутентификация** — получение `access_token` и `refresh_token` через Keycloak.
- **Обновление токена** — обмен `refresh_token` на новый `access_token`.
- **Получение профиля** — чтение данных пользователя по UUID.
- **Обновление профиля** — частичное обновление данных пользователя (username).
- **Health Check** — эндпоинт для мониторинга состояния сервиса.

---

## Архитектура

Проект следует **DDD (Domain-Driven Design)** с разделением на слои:

```
app/
├── api/            # Транспортный слой: HTTP-роутеры FastAPI, зависимости (DI)
│   └── v1/
│       ├── auth.py     # Эндпоинты: /auth/register, /auth/login, /auth/refresh
│       └── users.py    # Эндпоинты: GET /users/{id}, PATCH /users/{id}
├── application/    # Слой приложения: Use Cases, DTO, абстрактные порты
│   └── user/
│       ├── use_cases.py  # Бизнес-сценарии: Register, Login, Refresh, Get, Update
│       ├── dto.py        # Pydantic-схемы входных/выходных данных
│       └── ports.py      # Абстракция для Keycloak-адаптера
├── domain/         # Доменный слой: сущности, исключения, абстракции репозиториев
│   └── user/
│       ├── entity.py     # Доменная сущность User
│       ├── repository.py # Абстрактный репозиторий
│       └── exceptions.py # UserAlreadyExistsError, UserNotFoundError
├── infrastructure/ # Инфраструктурный слой: реализации репозиториев, Keycloak-клиент
│   └── keycloak/
└── core/           # Конфигурация, настройки приложения
```

Такое разделение гарантирует, что бизнес-логика (domain + application) не зависит от деталей реализации (FastAPI, SQLAlchemy, Keycloak).

---

## Технологический стек

| Компонент       | Технология                  |
|-----------------|-----------------------------|
| Framework       | FastAPI 0.115                |
| ASGI-сервер     | Uvicorn                      |
| Валидация       | Pydantic v2                  |
| ORM             | SQLAlchemy 2.0 (asyncio)     |
| БД драйвер      | asyncpg                      |
| Миграции        | Alembic                      |
| Аутентификация  | Keycloak 24 + python-keycloak|
| HTTP-клиент     | httpx                        |
| Логирование     | structlog                    |
| Линтер/типизация| ruff + mypy                  |
| Тесты           | pytest                       |

---

## Требования

- **Docker** и **Docker Compose** — для запуска через контейнеры
- **Python 3.12+** — для локальной разработки без Docker
- **Poetry** (опционально) — для управления зависимостями локально

---

## Быстрый старт (Docker Compose)

Это самый простой способ поднять все необходимые компоненты: приложение, PostgreSQL и Keycloak.

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/SashaFlake/to-do-list-user-backend.git
cd to-do-list-user-backend
```

### 2. Создайте файл `.env`

```bash
cp .env.example .env
```

При необходимости отредактируйте `.env` (подробнее — в разделе [Переменные окружения](#переменные-окружения)).

### 3. Запустите сервисы

```bash
docker compose up --build
```

После запуска будут доступны:

| Сервис         | URL                          |
|----------------|------------------------------|
| User Service   | http://localhost:8000        |
| Swagger UI     | http://localhost:8000/docs   |
| ReDoc          | http://localhost:8000/redoc  |
| Keycloak Admin | http://localhost:8080        |
| PostgreSQL     | localhost:5432               |

### 4. Выполните миграции

```bash
docker compose exec app alembic upgrade head
```

### 5. Настройте Keycloak

После первого запуска необходимо настроить realm и клиент в Keycloak:

1. Откройте http://localhost:8080 и войдите под `admin / admin`.
2. Создайте новый **Realm** (или используйте `master`).
3. Создайте **Client** с `client_id = user-service`, тип `confidential`.
4. Включите **Direct Access Grants** для поддержки логина по паролю.
5. Скопируйте `client_secret` и обновите его в `.env`.

---

## Локальная разработка

### 1. Установите зависимости

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Или через Poetry:

```bash
poetry install
```

### 2. Запустите инфраструктуру (БД и Keycloak)

```bash
docker compose up db keycloak -d
```

### 3. Примените миграции

```bash
make migrate
```

### 4. Запустите сервер с hot-reload

```bash
make dev
```

Сервис будет доступен на http://localhost:8000.

---

## Переменные окружения

| Переменная              | Описание                                      | Пример значения                                    |
|-------------------------|-----------------------------------------------|----------------------------------------------------|
| `APP_ENV`               | Окружение запуска                             | `development`                                      |
| `APP_HOST`              | Хост приложения                               | `0.0.0.0`                                          |
| `APP_PORT`              | Порт приложения                               | `8000`                                             |
| `APP_DEBUG`             | Режим отладки                                 | `true`                                             |
| `DATABASE_URL`          | URL подключения к PostgreSQL (asyncpg)        | `postgresql+asyncpg://user:password@localhost:5432/users_db` |
| `KEYCLOAK_SERVER_URL`   | URL сервера Keycloak                          | `http://localhost:8080`                            |
| `KEYCLOAK_REALM`        | Название realm в Keycloak                     | `master`                                           |
| `KEYCLOAK_CLIENT_ID`    | ID клиента в Keycloak                         | `user-service`                                     |
| `KEYCLOAK_CLIENT_SECRET`| Секрет клиента Keycloak                       | `secret`                                           |
| `KEYCLOAK_ADMIN_USERNAME`| Имя администратора Keycloak                  | `admin`                                            |
| `KEYCLOAK_ADMIN_PASSWORD`| Пароль администратора Keycloak               | `admin`                                            |

---

## Миграции базы данных

Проект использует **Alembic** для управления схемой БД.

```bash
# Применить все миграции до последней
make migrate

# Создать новую авто-миграцию (замените "description" на описание изменения)
make migrate-auto msg="add user table"

# Или напрямую через alembic
alembic upgrade head
alembic revision --autogenerate -m "your message"
```

---

## API Reference

Базовый URL: `http://localhost:8000/api/v1`

### Auth

#### `POST /auth/register` — Регистрация пользователя

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "strongpass123"
}
```

**Ответ `201 Created`:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

**Ошибки:** `409 Conflict` — пользователь с таким email уже существует.

---

#### `POST /auth/login` — Аутентификация

**Тело запроса:**
```json
{
  "email": "user@example.com",
  "password": "strongpass123"
}
```

**Ответ `200 OK`:**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Ошибки:** `401 Unauthorized` — неверные учётные данные.

---

#### `POST /auth/refresh` — Обновление токена

**Тело запроса:**
```json
{
  "refresh_token": "eyJhbGci..."
}
```

**Ответ `200 OK`:** аналогичен `/auth/login`.

**Ошибки:** `401 Unauthorized` — токен истёк или недействителен.

---

### Users

#### `GET /users/{user_id}` — Получение профиля пользователя

**Параметры:** `user_id` (UUID) — идентификатор пользователя.

**Ответ `200 OK`:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

**Ошибки:** `404 Not Found` — пользователь не найден.

---

#### `PATCH /users/{user_id}` — Обновление профиля

**Параметры:** `user_id` (UUID).

**Тело запроса (все поля опциональны):**
```json
{
  "username": "new_username"
}
```

**Ответ `200 OK`:** обновлённый профиль пользователя.

**Ошибки:** `404 Not Found` — пользователь не найден.

---

### Health Check

#### `GET /health`

**Ответ `200 OK`:**
```json
{
  "status": "ok"
}
```

---

## Тестирование

```bash
make test
# или
pytest tests/ -v
```

Линтинг и проверка типов:

```bash
make lint
# эквивалентно: ruff check . && mypy app
```

---

## Структура проекта

```
.
├── app/
│   ├── api/                  # HTTP-слой, роутеры, DI-зависимости
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       └── router.py
│   ├── application/          # Use Cases, DTO, порты (интерфейсы)
│   │   └── user/
│   ├── domain/               # Доменные сущности, репозитории, исключения
│   │   └── user/
│   ├── infrastructure/       # SQLAlchemy-репозитории, Keycloak-адаптер
│   ├── core/                 # Конфигурация приложения
│   └── main.py               # Точка входа FastAPI
├── migrations/               # Alembic-миграции
├── tests/                    # Тесты
├── .env.example              # Пример конфигурации окружения
├── docker-compose.yml        # Оркестрация контейнеров
├── Dockerfile
├── Makefile                  # Утилиты: dev, lint, test, migrate
├── alembic.ini
├── pyproject.toml
└── requirements.txt
```
