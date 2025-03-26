# Tron Wallet Info Service

Микросервис для получения информации о кошельках в сети Tron (TRX баланс, bandwidth, energy)

## Функциональность

- Получение информации о кошельке по адресу
- История запросов с пагинацией
- Кэширование запросов
- Мониторинг через Elasticsearch/Kibana

## Технологии

- Python 3.11
- FastAPI
- SQLAlchemy
- База для кэширования Redis
- База для логирования Elasticsearch/Kibana
- Docker 

## Быстрый старт

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Приложение будет доступно на http://localhost:8000
```

## Или при использовании Docker

### Требования

- Docker 20+
- Docker Compose 1.29+

### Запуск в development режиме

```bash
git clone https://github.com/shido-backend/tron_api
cd tron-wallet-service

# Запускаем сервисы
docker-compose up -d --build

# Приложение будет доступно на http://localhost:8000
```

### API Endpoints

- `POST /api/wallet-info/` - Получить информацию о кошельке
- `GET /api/query-history/` - История запросов
- `GET /api/docs` - Swagger документация

### Production сборка

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## Дополнительные команды

```bash
# Просмотр логов
docker-compose logs -f app

# Остановка всех сервисов
docker-compose down

# Очистка данных
docker-compose down -v
```