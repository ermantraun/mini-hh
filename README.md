# Resume Service (Clean Architecture + Dishka)

Полноценный сервис резюме:

- Регистрация / авторизация (JWT)
- CRUD резюме
- Улучшение текста (заглушка: добавляет ` [Improved]`)
- История улучшений
- Чистая архитектура (domain / application / infrastructure / api)
- DI: Dishka
- PostgreSQL + Alembic
- Тесты (pytest, httpx)
- Логирование
- Docker / Compose

## Архитектура

```
api/            # Транспорт (FastAPI), DI контейнер, конфигурация
application/    # DTO, интерфейсы, интеракторы (use cases), безопасность
domain/         # Доменные сущности (dataclass)
infrastructure/ # Модели БД, репозитории, миграции Alembic
tests/          # Pytest E2E
```

## Запуск (локально)

1. Создайте и заполните `.env` (см. `.env.example`) либо используйте переменные окружения.
2. Установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn api.main:app --reload
```

Документация: http://localhost:8000/docs

## Docker

```bash
docker compose up --build
```

Сервисы:

- db: PostgreSQL
- api: FastAPI на http://localhost:8000
- frontend: Vite dev сервер на http://localhost:5173

Frontend запускается без Dockerfile, через контейнер node (volume монтирует папку `frontend`).
Фронтенд делает прямые запросы к API по адресу http://localhost:8000 (CORS в API разрешён для всех источников).

## Тесты

```bash
pytest -q
```

(При необходимости задайте отдельную тестовую БД через `POSTGRES_DB_TEST`.)

### Тестовый режим (pytest)

При запуске `pytest`:

- Автоматически используются in-memory репозитории (без PostgreSQL).
- Соединение с БД не создаётся — контейнер DI подменяет реализации на `InMemory*Repository`.
- Авторизация упрощена: если заголовок `Authorization` отсутствует, используется `user_id=1`.
- Это поведение предназначено только для тестов и не должно применяться в продакшене.

Чтобы проверить работу с реальной БД — запускайте приложение обычным способом (uvicorn / docker), где задействованы реальные репозитории и JWT.

## Переменные окружения

| Переменная        | Описание                   | Значение по умолчанию |
| --------------------------- | ---------------------------------- | ---------------------------------------- |
| POSTGRES_HOST               | Хост БД                      | db                                       |
| POSTGRES_PORT               | Порт                           | 5432                                     |
| POSTGRES_USER               | Пользователь           | resume                                   |
| POSTGRES_PASSWORD           | Пароль                       | resume                                   |
| POSTGRES_DB                 | База                           | resume                                   |
| JWT_SECRET_KEY              | Секрет JWT                   | change_me                                |
| ACCESS_TOKEN_EXPIRE_MINUTES | Время жизни токена | 1440                                     |
| LOG_LEVEL                   | Уровень логов          | INFO                                     |

## Эндпоинты

- POST /auth/register
- POST /auth/login
- POST /resumes
- GET /resumes
- GET /resumes/{id}
- PUT /resumes/{id}
- DELETE /resumes/{id}
- POST /resumes/{id}/improvements/improve
- GET /resumes/{id}/improvements

Авторизация: заголовок `Authorization: Bearer <token>`

> В тестовом режиме (pytest) заголовок можно не передавать — будет выбран пользователь 1.

---

## Фронтенд

Проект фронтенда (React + Vite + TypeScript) в каталоге `frontend`.

Локальный запуск:

- Node.js 18+
- Команды:
  - npm install
  - npm run dev
- Откройте: http://localhost:5173

Интеграция с API:

- Запросы идут напрямую на http://localhost:8000 (см. `src/pages/Home.tsx`).
- Никакого прокси не используется.

CORS:

- В API включён CORS для всех источников (`api/main.py`, `CORSMiddleware`), поэтому прямые запросы с http://localhost:5173 к http://localhost:8000 работают.

Скрипты фронтенда:

- npm run dev — запуск dev-сервера (порт 5173)
- npm run build — сборка прод-версии
- npm run preview — предпросмотр сборки
