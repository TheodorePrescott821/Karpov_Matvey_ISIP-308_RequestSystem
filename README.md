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

## 🔌 REST API

### Запуск и Доступ

API автоматически запускается при команде `docker-compose up -d --build`.

**API Адрес:** `http://localhost:8000`

**Интерактивная документация (выбери один из вариантов):**
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

> 💡 **Совет:** Используйте Swagger UI (`/docs`) для интерактивного тестирования API - можно отправлять запросы прямо из браузера

### 📋 Основные Endpoints

#### Health Check (Проверка здоровья)

```
GET /health
```
- Проверка статуса приложения (используется Docker и Kubernetes)
- **Ответ:** `{"status": "healthy"}` (HTTP 200)

```
GET /ready
```
- Проверка готовности приложения
- **Ответ:** `{"ready": true}` (HTTP 200)

#### Управление Запросами (Requests)

```
GET /api/requests
```
- **Описание:** Получить список всех запросов с фильтрацией, поиском и сортировкой
- **Параметры запроса:**
  - `status` - Фильтр по статусу (New, In Progress, Under Review, Approved, Rejected, Completed)
  - `priority` - Фильтр по приоритету (Low, Medium, High, Critical)
  - `user_id` - Фильтр по ID пользователя (заявитель)
  - `category_id` - Фильтр по ID категории
  - `account_name` - Фильтр по имени учетной записи
  - `search` - Полнотекстовый поиск по описанию и имени пользователя
  - `search_description` - Поиск только в описании
  - `sort_by` - Сортировка по полю (created_at, id, priority, status, account_name)
  - `sort_order` - Порядок сортировки (asc, desc)
  - `limit` - Количество результатов (1-100, по умолчанию 10)
  - `offset` - Смещение для пагинации (по умолчанию 0)
  - `page` - Номер страницы (альтернатива offset)

**Ответ:**
```json
{
  "requests": [
    {
      "request_id": 1,
      "request_number": "REQ-001",
      "description": "Установка ПО",
      "applicant_user_id": 1,
      "user_name": "Иван Петров",
      "category_id": 2,
      "category_name": "IT",
      "priority": "High",
      "status": "In Progress",
      "registered_at": "2026-11-17T10:30:00"
    }
  ],
  "total_count": 42,
  "filtered_count": 15,
  "returned_count": 10,
  "limit": 10,
  "offset": 0,
  "has_next": true,
  "has_previous": false
}
```

### 📝 Примеры Запросов

#### 1️⃣ Получить все запросы (базовый запрос)

```bash
curl "http://localhost:8000/api/requests"
```

#### 2️⃣ Получить запросы со статусом "In Progress"

```bash
curl "http://localhost:8000/api/requests?status=In%20Progress"
```

#### 3️⃣ Поиск по описанию (полнотекстовый поиск)

```bash
curl "http://localhost:8000/api/requests?search=laptop"
```

#### 4️⃣ Фильтрация: высокий приоритет и "In Progress", сортировка по новизне

```bash
curl "http://localhost:8000/api/requests?priority=High&status=In%20Progress&sort_by=created_at&sort_order=desc&limit=20"
```

#### 5️⃣ Пагинация: вторая страница с 20 элементами

```bash
curl "http://localhost:8000/api/requests?limit=20&page=2"
```

#### 6️⃣ Поиск по ID пользователя (заявители)

```bash
curl "http://localhost:8000/api/requests?user_id=1"
```

#### 7️⃣ Поиск только в описании

```bash
curl "http://localhost:8000/api/requests?search_description=equipment"
```

#### 8️⃣ Фильтрация по имени пользователя

```bash
curl "http://localhost:8000/api/requests?account_name=john"
```

### 🧪 Тестирование в Swagger UI

1. Откройте http://localhost:8000/docs
2. Нажмите на **GET /api/requests**
3. Нажмите **"Try it out"**
4. Добавьте параметры (опционально)
5. Нажмите **"Execute"**

### ⚠️ Значения параметров

**Status (Статус):**
- `New` - Новая заявка
- `In Progress` - В процессе выполнения
- `Under Review` - На рассмотрении
- `Approved` - Одобрена
- `Rejected` - Отклонена
- `Completed` - Завершена

**Priority (Приоритет):**
- `Low` - Низкий
- `Medium` - Средний
- `High` - Высокий
- `Critical` - Критический

### 🔄 Коды ответов

- **200 OK** - Успешный запрос
- **400 Bad Request** - Неверные параметры
- **422 Unprocessable Entity** - Неверные значения параметров
- **503 Service Unavailable** - Сервис недоступен

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
