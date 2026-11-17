# Система обработки заявок (Request System)

Полнофункциональное веб-приложение для управления заявками и запросами на услуги в организациях.

## Назначение

Система предназначена для:
- **Заявителей:** Регистрировать запросы на услуги и отслеживать их статус
- **Операторов:** Проверять поступившие заявки и назначать исполнителей
- **Исполнителей:** Выполнять работы и фиксировать ход их выполнения
- **Контролеров:** Проверять результаты и принимать или возвращать на доработку

## Основные функции

### 1. Управление заявками
- Регистрация новых заявок с описанием, категорией и приоритетом
- Просмотр всех заявок с фильтрацией по статусу, категории и приоритету
- Полнотекстовый поиск по описанию заявок
- Просмотр подробной информации о каждой заявке
- Редактирование параметров заявки
- Удаление заявок из системы

### 2. Отслеживание статуса
- Просмотр истории изменения статуса заявки
- Обновление статуса в реальном времени
- Визуализация жизненного цикла заявки

### 3. Поиск и фильтрация
- Расширенный поиск по полнотекстовому индексу
- Фильтрация по статусу, категории, приоритету
- Пагинация результатов
- Сортировка по различным полям

### 4. Управление распределением
- Назначение исполнителей на заявки
- Отслеживание времени выполнения
- История всех назначений и изменений

## Технический стек

- **Backend:** Python FastAPI с асинхронной обработкой
- **БД:** SQLite (разработка) / PostgreSQL (production)
- **Cache:** Redis
- **Контейнеризация:** Docker & Docker Compose
- **API:** REST с OpenAPI/Swagger документацией

## Быстрый старт

### Требования

- **Docker Desktop** (или Docker + Docker Compose)
- **Git** для клонирования репозитория
- **8GB RAM** (рекомендуется)
- **1GB свободного места на диске**

### Локальное развертывание (Docker)

#### 1️⃣ Клонировать репозиторий

```bash
git clone https://github.com/TheodorePrescott821/Karpov_Matvey_ISIP-308_RequestSystem.git
cd Karpov_Matvey_ISIP-308_RequestSystem
```

#### 2️⃣ Запустить контейнеры

```bash
docker-compose up -d --build
```

Эта команда:
- Создаст Docker образ приложения
- Запустит три контейнера:
  - **API сервер** (FastAPI)
  - **PostgreSQL** база данных
  - **Redis** кэш

#### 3️⃣ Проверить статус

```bash
docker-compose ps
```

Все контейнеры должны иметь статус **Up**.

#### 4️⃣ Просмотр логов

```bash
# Логи всех сервисов
docker-compose logs -f

# Логи только API
docker-compose logs -f app

# Логи только БД
docker-compose logs -f db
```

### 🌐 Доступ к приложению

| Сервис | URL | Описание |
|--------|-----|---------|
| **API** | http://localhost:8000 | REST API (JSON) |
| **Swagger UI** | http://localhost:8000/docs | Интерактивная документация API |
| **ReDoc** | http://localhost:8000/redoc | Альтернативная документация |
| **PostgreSQL** | localhost:5432 | База данных |
| **Redis** | localhost:6379 | Кэш памяти |

### 📝 Переменные окружения

Создайте файл `.env` в корне проекта для кастомизации:

```bash
# APP
APP_PORT=8000
APP_ENV=development
APP_DEBUG=true

# DATABASE
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=requests_db
DB_PORT=5432

# REDIS
REDIS_PORT=6379
REDIS_MAX_MEMORY=256mb
```

Если файл не создавать, используются значения по умолчанию из `docker-compose.yml`.

### ⛔ Остановка приложения

```bash
# Остановить контейнеры (сохранить данные)
docker-compose stop

# Удалить контейнеры (сохранить данные)
docker-compose down

# Полная очистка (удалить данные и образы)
docker-compose down -v
```

### 🔧 Часто используемые команды

```bash
# Перестроить и запустить
docker-compose up -d --build

# Пересоздать контейнеры
docker-compose down && docker-compose up -d

# Выполнить команду в контейнере API
docker-compose exec app bash

# Просмотреть размер данных БД
docker-compose exec db du -sh /var/lib/postgresql/data
```

### ✅ Проверка здоровья приложения

```bash
# Запрос к API
curl http://localhost:8000/health

# Проверка Swagger UI в браузере
# Откройте http://localhost:8000/docs и попробуйте запрос
```

### 🐛 Решение проблем

**Ошибка: "Port 8000 is already in use"**
```bash
# Измените порт в .env файле
APP_PORT=8001
docker-compose up -d
```

**Ошибка: "Cannot connect to Docker daemon"**
- Убедитесь, что Docker Desktop запущен
- На Linux: проверьте права доступа к Docker сокету

**Контейнер API постоянно перезагружается**
```bash
docker-compose logs app  # Просмотр ошибок
```

## API Эндпоинты

### Запросы (Requests)
- `GET /api/v1/requests` - Получить все запросы
- `POST /api/v1/requests` - Создать новый запрос
- `GET /api/v1/requests/{id}` - Получить запрос по ID
- `PUT /api/v1/requests/{id}` - Обновить запрос
- `DELETE /api/v1/requests/{id}` - Удалить запрос

**Параметры фильтрации:**
- `status` - Фильтр по статусу
- `category` - Фильтр по категории
- `priority` - Фильтр по приоритету
- `search` - Поиск по описанию
- `limit` - Лимит результатов (по умолчанию 10)
- `offset` - Смещение для пагинации

### Пример запроса

```bash
# Получить все открытые запросы с высоким приоритетом
curl "http://localhost:8000/api/v1/requests?status=open&priority=high"

# Поиск запроса
curl "http://localhost:8000/api/v1/requests?search=installation"

# Создать новый запрос
curl -X POST http://localhost:8000/api/v1/requests \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Установка ПО",
    "description": "Требуется установить Office 365",
    "category": "IT",
    "priority": "high"
  }'
```

## Структура проекта

```
├── src/request_system/          # Основной код
│   ├── domain/                  # Бизнес-логика (сущности)
│   ├── application/             # Сервисы и случаи использования
│   ├── infrastructure/          # Работа с БД и сторонними сервисами
│   └── presentation/            # REST API и main.py
├── docs/                        # Документация
│   ├── DEPLOYMENT.md            # Руководство по развертыванию
│   ├── DATABASE_SCHEMA.md       # Схема БД
│   └── API-TESTING-GUIDE.md     # Примеры API запросов
├── tests/                       # Автоматизированные тесты
├── docker-compose.yml           # Конфигурация Docker
└── Dockerfile                   # Образ приложения
```

## Требования

- Python 3.9+
- Docker & Docker Compose (для контейнеризации)
- PostgreSQL 12+ (production)
- Redis 6+ (production)

## Разработка

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск локально (без Docker)

```bash
export DATABASE_URL="sqlite:///./requests.db"
python -m uvicorn src.request_system.presentation.main:app --reload
```

## Документация

- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Развертывание на VPS
- [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) - Схема БД
- [docs/API-TESTING-GUIDE.md](docs/API-TESTING-GUIDE.md) - Примеры API
- [docs/search-and-filtering.md](docs/search-and-filtering.md) - Поиск и фильтрация

## Лицензия

MIT
