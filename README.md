# Wallet Check

Микросервис на FastAPI для получения информации о кошельке в сети Tron с последующей записью этой информации в БД.

## Описание

Представляет два эндпоинта:
1. **GET /api/v1/wallets** - для получения информации из БД о кошельках.
2. **POST /api/v1/balance** - для получения информации о кошельке из ***TronScan*** и записи этой информации в БД.

## Установка

1. Клонируем репоизторий и переходим в директорию с ним:

```
git clone адресс_репозитория
cd ./имя_директории_с_проектом
```

2. Создаем и активируем виртуальное окружение:

```
python -m venv venv
.\venv\Scripts\activate
```

3. Устанавливаем зависимости:

```
pip install -r requirements.txt
```

4. Создаем файл ***.env*** и задаем в нем переменную **API_KEY**:


    API_KEY = "ваш_ключ"


API-ключ можно получить [здесь](https://tronscan.org/#/myaccount/apiKeys/)

5. Запускаем приложение:

```
uvicorn main:app
```

## Тестирование

Для запуска тестов используйте следующую команду:

```
pytest .\tests\test_endpoints.py
```

## Документация API

   Документация доступна по [этой](http://localhost:8000/docs) ссылке