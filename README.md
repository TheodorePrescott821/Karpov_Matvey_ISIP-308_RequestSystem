# Система обработки заявок (Request System)

Полнофункциональное веб-приложение для управления заявками и запросами на услуги в организациях.

## 📋 Назначение

Система предназначена для:
- **Заявителей:** Регистрировать запросы на услуги и отслеживать их статус
- **Операторов:** Проверять поступившие заявки и назначать исполнителей
- **Исполнителей:** Выполнять работы и фиксировать ход их выполнения
- **Контролеров:** Проверять результаты и принимать или возвращать на доработку

## ✨ Основные функции

### 1. Управление заявками
- 📝 Регистрация новых заявок с описанием, категорией и приоритетом
- 🔍 Просмотр всех заявок с фильтрацией по статусу, категории и приоритету
- 🔎 Полнотекстовый поиск по описанию заявок
- 📊 Просмотр подробной информации о каждой заявке
- ✏️ Редактирование параметров заявки
- 🗑️ Удаление заявок из системы

### 2. Отслеживание статуса
- 📅 Просмотр истории изменения статуса заявки
- 🔄 Обновление статуса в реальном времени
- 📈 Визуализация жизненного цикла заявки

### 3. Поиск и фильтрация
- 🔍 Расширенный поиск по полнотекстовому индексу
- 🏷️ Фильтрация по статусу, категории, приоритету
- 📄 Пагинация результатов
- 📊 Сортировка по различным полям

### 4. Управление распределением
- 👥 Назначение исполнителей на заявки
- ⏱️ Отслеживание времени выполнения
- 📋 История всех назначений и изменений

## Технический стек

- **Backend:** Python FastAPI с асинхронной обработкой
- **БД:** SQLite (разработка) / PostgreSQL (production)
- **Cache:** Redis
- **Контейнеризация:** Docker & Docker Compose
- **API:** REST с OpenAPI/Swagger документацией

## Быстрый старт

### Локальное развертывание (Docker)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/TheodorePrescott821/Karpov_Matvey_ISIP-308_RequestSystem.git
cd Karpov_Matvey_ISIP-308_RequestSystem

# 2. Запустить контейнеры
docker-compose up -d --build

# 3. Проверить статус
docker-compose ps
```

**Доступ:**
- API Swagger UI: http://localhost:8000/docs
- API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

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
