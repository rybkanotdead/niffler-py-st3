# Niffler - E2E тесты на Python

## Содержание

- [Технологии и инструменты](#технологии-и-инструменты)
- [Структура проекта](#структура-проекта)
- [Список тестов](#список-тестов)
- [Запуск тестов](#запуск-тестов)
- [Allure отчёт](#allure-отчёт)

---

## Технологии и инструменты

| Инструмент | Описание |
|:----------:|:---------|
| Python 3.11 | Язык программирования |
| Pytest | Фреймворк для тестирования |
| Selene | UI автоматизация (обёртка над Selenium) |
| Selenium | WebDriver для браузерного тестирования |
| Requests | HTTP клиент для REST API тестов |
| PostgreSQL | Реляционная БД |
| psycopg2 | Драйвер для работы с PostgreSQL |
| Pydantic | Валидация данных и type hints |
| Faker | Генерация тестовых данных |
| Allure | Отчётность по тестам |
| Poetry | Менеджер зависимостей |
| pytest-xdist | Параллельный запуск тестов |

---

## Структура проекта

```
niffler-e2e-tests-python/
│
├── clients/                          # HTTP клиенты
│   ├── __init__.py
│   ├── api.py                        # BaseHttpClient, CategoryApiClient, SpendApiClient
│   └── spends_client.py              # Legacy клиент
│
├── config.py                         # Конфигурация приложения (@dataclass + singleton)
│
├── conftest.py                       # Фикстуры pytest
│
├── databases/                        # Модели БД
│   ├── __init__.py
│   └── spend_db.py
│
├── helpers/                          # Вспомогательные утилиты
│   ├── __init__.py
│   └── db_client.py                  # DBClient — работа с PostgreSQL
│
├── modals/                           # Pydantic-модели
│   ├── __init__.py
│   ├── category.py
│   ├── config.py
│   └── spend.py
│
├── pages/                            # Page Objects
│   ├── __init__.py
│   ├── auth_reg_page.py              # Страница авторизации и регистрации
│   ├── category_page.py              # Страница категорий
│   ├── profile_page.py               # Страница профиля
│   └── spendings_page.py             # Страница трат
│
├── tests/                            # Тесты
│   ├── __init__.py
│   ├── test_auth_page.py             # Тесты авторизации
│   ├── test_registation_page.py      # Тесты регистрации
│   ├── test_profile_page.py          # Тесты профиля
│   ├── test_spending_page.py         # Тесты трат (UI)
│   ├── test_db_integration.py        # Интеграционные тесты UI + БД
│   ├── test_api_with_db.py           # Интеграционные тесты API + БД
│   └── test_real_run.py              # Unit-тесты фреймворка
│
├── pyproject.toml                    # Poetry конфигурация
├── poetry.lock
├── .env                              # Переменные окружения
└── README.md
```

---

## Список тестов

### UI тесты

| Тест | Описание |
|:-----|:---------|
| `test_auth_page.py` | Авторизация пользователя через UI |
| `test_registation_page.py` | Регистрация нового пользователя |
| `test_profile_page.py` | Работа с профилем (категории, архивация) |
| `test_spending_page.py` | Создание, редактирование и удаление трат |

### Интеграционные тесты UI + БД

| Тест | Описание |
|:-----|:---------|
| `test_create_category_via_ui_verify_in_db` | Создание категории через UI → проверка в БД |
| `test_archive_category_check_db_state` | Архивация категории через UI → проверка флага `archived` в БД |
| `test_create_empty_category_name_error` | Попытка создать категорию с пустым именем (негативный) |
| `test_create_spending_via_ui_verify_in_db` | Создание траты через UI → проверка в БД |
| `test_delete_spending_via_ui_verify_in_db` | Удаление траты через UI → проверка отсутствия в БД |
| `test_add_spending_zero_amount_validation` | Попытка создать трату с нулевой суммой (негативный) |

### Интеграционные тесты API + БД

| Тест | Описание |
|:-----|:---------|
| `test_create_category_via_api_verify_in_db` | Создание категории через API → проверка в БД |
| `test_get_categories_api_matches_db` | Получение категорий через API → сравнение с БД |
| `test_create_spending_via_api_verify_in_db` | Создание траты через API → проверка в БД |
| `test_delete_spending_via_api_verify_in_db` | Удаление траты через API → проверка отсутствия в БД |
| `test_get_spendings_api_matches_db` | Получение трат через API → сравнение с БД |

---

## Запуск тестов

### Предварительные условия

1. Установить зависимости:
```bash
poetry install
```

2. Настроить `.env` файл:
```dotenv
AUTH_URL=http://auth.niffler.dc:9000
FRONTEND_URL=http://frontend.niffler.dc
GATEWAY_URL=http://gateway.niffler.dc:8090
PROFILE_URL=http://frontend.niffler.dc/profile
SPEND_DB_URL=postgresql://postgres:secret@localhost:5432/niffler-spend
TEST_USERNAME=your_username
TEST_PASSWORD=your_password
```

3. Запустить инфраструктуру Niffler (Docker Compose)

### Команды запуска

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Параллельно (4 процесса)
pytest -n 4

# Только UI тесты
pytest -m ui

# Только API тесты
pytest -m api

# Только DB тесты
pytest -m db

# С генерацией Allure отчёта
pytest --alluredir=allure-results
```

---

## Allure отчёт

### Генерация отчёта

```bash
# Запуск тестов с сохранением результатов
pytest --alluredir=allure-results

# Открыть отчёт в браузере
allure serve allure-results
```

### Пример отчёта

Отчёт содержит:
- Общую статистику прохождения тестов
- Детализацию по каждому тесту с шагами (`allure.step`)
- Скриншоты при падении тестов
- Логи и вложения
- Историю запусков

---

## Архитектура

### Config (`config.py`)
Централизованная конфигурация через `@dataclass` с паттерном Singleton.
Все параметры загружаются из `.env` файла.

### HTTP клиенты (`clients/api.py`)
Иерархия клиентов с базовым классом `BaseHttpClient`:
- `CategoryApiClient` — CRUD операции с категориями
- `SpendApiClient` — CRUD операции с тратами
- Поддержка context manager (`with`)

### БД клиент (`helpers/db_client.py`)
Работа с PostgreSQL через `psycopg2`:
- CRUD для категорий и трат
- Очистка тестовых данных
- Type hints для всех методов

### Page Objects (`pages/`)
Паттерн Page Object для UI тестов:
- `AuthRegistrationPage` — авторизация и регистрация
- `ProfilePage` — профиль пользователя
- `SpendingPage` — страница трат

### Фикстуры (`conftest.py`)
Организация по слоям:
- **Session scope** — конфигурация, БД, API клиенты
- **Function scope** — браузер, Page Objects, авторизация, генерация данных
- **Cleanup** — автоматическая очистка тестовых данных после каждого теста
