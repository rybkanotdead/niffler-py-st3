# Niffler - E2E тесты на Python

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-7.x-green?logo=pytest)
![Allure](https://img.shields.io/badge/Allure-Report-orange)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-black?logo=github-actions)

## Содержание

- [Технологии и инструменты](#технологии-и-инструменты)
- [Структура проекта](#структура-проекта)
- [Покрытие тестами](#покрытие-тестами)
- [Запуск тестов](#запуск-тестов)
- [Allure отчёт](#allure-отчёт)
- [GitHub Actions](#github-actions)

---

## Технологии и инструменты

| Инструмент | Описание |
|:----------:|:---------|
| Python 3.11 | Язык программирования |
| Pytest | Фреймворк для тестирования |
| Selene | UI автоматизация (обёртка над Selenium) |
| Selenium | WebDriver для браузерного тестирования |
| Requests | HTTP клиент для REST API тестов |
| gRPC / protobuf | Тестирование Currency gRPC сервиса |
| Requests + XML | SOAP тесты Userdata сервиса |
| kafka-python | Тесты Kafka событий (топик `users`) |
| PostgreSQL | Реляционная БД |
| psycopg2 | Драйвер для работы с PostgreSQL |
| Pydantic | Валидация данных и type hints |
| Faker | Генерация тестовых данных |
| Allure | Отчётность по тестам |
| Poetry | Менеджер зависимостей |
| pytest-xdist | Параллельный запуск тестов |
| GitHub Actions | CI/CD и деплой Allure отчётов |

---

## Структура проекта

```
niffler-e2e-tests-python/
│
├── clients/                          # Клиенты для взаимодействия с сервисами
│   ├── __init__.py
│   ├── api.py                        # REST API: CategoryApiClient, SpendApiClient
│   ├── grpc_client.py                # gRPC клиент: CurrencyGrpcClient
│   ├── soap_client.py                # SOAP клиент: UserdataSoapClient
│   ├── kafka_client.py               # Kafka клиент: KafkaClient
│   └── grpc_stubs/                   # Сгенерированные gRPC стабы
│       ├── niffler-currency.proto
│       ├── niffler_currency_pb2.py
│       └── niffler_currency_pb2_grpc.py
│
├── config.py                         # Конфигурация (@dataclass + singleton)
├── conftest.py                       # Фикстуры pytest
│
├── helpers/                          # Вспомогательные утилиты
│   ├── __init__.py
│   └── db_client.py                  # DBClient — работа с PostgreSQL
│
├── modals/                           # Pydantic-модели
│   ├── __init__.py
│   ├── category.py
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
│   ├── test_auth_page.py             # UI: авторизация
│   ├── test_registation_page.py      # UI: регистрация
│   ├── test_profile_page.py          # UI: профиль и категории
│   ├── test_spending_page.py         # UI: траты
│   ├── test_db_integration.py        # UI/API + БД интеграционные тесты
│   ├── test_api_with_db.py           # REST API + БД тесты
│   ├── test_grpc.py                  # gRPC: Currency сервис
│   ├── test_soap.py                  # SOAP: Userdata сервис
│   └── test_kafka.py                 # Kafka: топик users
│
├── pyproject.toml                    # Зависимости проекта (Poetry)
├── .env                              # Переменные окружения (не коммитить!)
├── env.default                       # Шаблон переменных окружения
└── README.md
```

---

## Покрытие тестами

### 🖥️ UI тесты (Selene + Selenium)

| Тест | Описание |
|:-----|:---------|
| `test_auth_page.py` | Авторизация пользователя через UI |
| `test_registation_page.py` | Регистрация нового пользователя |
| `test_profile_page.py` | Работа с профилем и категориями |
| `test_spending_page.py` | Создание, редактирование и удаление трат |

### 🔌 REST API + БД тесты

| Тест | Описание |
|:-----|:---------|
| `test_create_category_via_api_verify_in_db` | Создание категории через API → проверка в БД |
| `test_get_categories_api_matches_db` | Сравнение категорий из API и БД |
| `test_create_spending_via_api_verify_in_db` | Создание траты через API → проверка в БД |
| `test_delete_spending_via_api_verify_in_db` | Удаление траты через API → проверка в БД |

### 🗄️ Интеграционные тесты UI + БД

| Тест | Описание |
|:-----|:---------|
| `test_create_category_via_ui_verify_in_db` | Создание категории через UI → проверка в БД |
| `test_archive_category_check_db_state` | Архивация категории → проверка флага `archived` |
| `test_create_spending_via_ui_verify_in_db` | Создание траты через UI → проверка в БД |
| `test_delete_spending_via_ui_verify_in_db` | Удаление траты через UI → проверка в БД |

### 📡 gRPC тесты (Currency сервис, порт 8092)

| Тест | Описание |
|:-----|:---------|
| `test_get_all_currencies` | Получение всех валют с курсами |
| `test_calculate_rate_rub_to_usd` | Конвертация RUB → USD |
| `test_calculate_rate_usd_to_rub` | Конвертация USD → RUB |
| `test_calculate_rate_same_currency` | Конвертация одинаковых валют |
| `test_calculate_rate_eur_to_kzt` | Конвертация EUR → KZT |

### 🧼 SOAP тесты (Userdata сервис, порт 8089)

| Тест | Описание |
|:-----|:---------|
| `test_get_current_user` | Получение данных пользователя |
| `test_update_user_name` | Обновление имени и фамилии |
| `test_get_all_users` | Получение списка пользователей |
| `test_current_user_response_structure` | Проверка структуры SOAP ответа |

### 📨 Kafka тесты (топик `users`, порт 9092)

| Тест | Описание |
|:-----|:---------|
| `test_users_topic_exists` | Проверка существования топика |
| `test_registration_publishes_kafka_event` | Регистрация → проверка события в Kafka |
| `test_kafka_message_structure` | Проверка структуры Kafka сообщений |

---

## Запуск тестов

### Предварительные условия

1. Установить зависимости:
```bash
cd niffler-e2e-tests-python
pip install grpcio grpcio-tools protobuf zeep kafka-python \
    pytest selene selenium python-dotenv faker pytest-xdist \
    requests pydantic psycopg2-binary sqlalchemy allure-pytest
```

2. Скопировать и настроить `.env`:
```bash
cp env.default .env
# Отредактировать .env
```

3. Запустить инфраструктуру (Docker Compose):
```bash
cd ..
docker-compose up -d
```

### Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|:-----------|:---------|:----------------------|
| `AUTH_URL` | URL авторизации | `http://auth.niffler.dc:9000` |
| `FRONTEND_URL` | URL фронтенда | `http://frontend.niffler.dc` |
| `GATEWAY_URL` | URL API Gateway | `http://gateway.niffler.dc:8090` |
| `PROFILE_URL` | URL профиля | `http://frontend.niffler.dc/profile` |
| `SPEND_DB_URL` | URL БД | `postgresql://postgres:secret@localhost:5432/niffler-spend` |
| `GRPC_HOST` | Хост gRPC сервера | `localhost` |
| `GRPC_PORT` | Порт gRPC сервера | `8092` |
| `SOAP_URL` | URL SOAP эндпоинта | `http://localhost:8089/ws` |
| `KAFKA_BOOTSTRAP_SERVERS` | Адрес Kafka брокера | `localhost:9092` |
| `TEST_USERNAME` | Логин тестового пользователя | — |
| `TEST_PASSWORD` | Пароль тестового пользователя | — |
| `HEADLESS` | Браузер без GUI | `false` |

### Команды запуска

```bash
# Все тесты
pytest tests/

# Параллельно (4 процесса)
pytest tests/ -n 4

# Только UI тесты
pytest tests/ -m ui

# Только REST API тесты
pytest tests/ -m api

# Только gRPC тесты
pytest tests/ -m grpc

# Только SOAP тесты
pytest tests/ -m soap

# Только Kafka тесты
pytest tests/ -m kafka

# Только тесты с БД
pytest tests/ -m db

# Smoke тесты
pytest tests/ -m smoke

# С Allure отчётом и параллельным запуском
pytest tests/ --alluredir=allure-results -n 4
```

---

## Allure отчёт

```bash
# Запуск тестов и сохранение результатов
pytest tests/ --alluredir=allure-results

# Открыть отчёт локально
allure serve allure-results

# Сгенерировать статический отчёт
allure generate allure-results -o allure-report --clean
allure open allure-report
```

---

## GitHub Actions

Workflow (`.github/workflows/tests.yml`) запускается:
- ✅ При пуше в `main`/`master`
- ✅ При Pull Request
- ✅ Вручную через `workflow_dispatch` с выбором маркеров тестов и параллелизма

### Настройка GitHub Secrets

В `Settings → Secrets → Actions` добавьте:

| Secret | Описание |
|:-------|:---------|
| `AUTH_URL` | URL авторизации |
| `FRONTEND_URL` | URL фронтенда |
| `GATEWAY_URL` | URL Gateway |
| `TEST_USERNAME` | Логин тестового пользователя |
| `TEST_PASSWORD` | Пароль тестового пользователя |

### GitHub Pages (Allure отчёт)

После каждого запуска Allure отчёт автоматически публикуется:

```
https://<username>.github.io/<repository>/
```

**Активация:**
`Settings → Pages → Source: Deploy from branch → gh-pages`

---

## Архитектура

```
┌─────────────────────── Тесты (tests/) ───────────────────────┐
│  test_ui  │  test_api_with_db  │  test_grpc  │ test_soap │ test_kafka │
└─────┬─────┴─────────┬──────────┴──────┬──────┴─────┬─────┴──────┬────┘
      │               │                 │             │            │
      ▼               ▼                 ▼             ▼            ▼
   Selene          api.py          grpc_client   soap_client  kafka_client
   (UI)           (REST)           (gRPC:8092)  (SOAP:8089)  (Kafka:9092)
      │               │
      ▼               ▼
   Browser         Gateway  ──► PostgreSQL
                  REST API      (db_client)
```
