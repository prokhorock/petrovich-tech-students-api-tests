# petrovich-tech-students-api-tests

Тестовое на QA Auto.  
Стенд: http://93.77.188.34/apidocs

Покрыл CRUD по `/student`: позитивные и негативные кейсы.  
Стек: pytest + requests + allure + xdist.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

В корне нужен `.env`:

```
BASE_URL=http://93.77.188.34
```

Тесты:

```bash
pytest
```

Параллельно:

```bash
pytest -n auto
```

## Allure

Результаты пишутся в `allure-results`.

```bash
allure serve allure-results
```

В отчёте есть epic «Студенты», steps и http-логи.

## Структура

- `src/clients` — HTTP-клиент
- `src/utils` — payload, waits, asserts, allure logger
- `tests` — позитивные / негативные тесты
- `conftest.py` — фикстуры

## Баги

Что нашёл по API:  
https://docs.google.com/spreadsheets/d/1PYdP2oZokkOvqkLIu3CehqCfOMiH-TAwvoPrN5y9I08/edit?usp=sharing
