# petrovich-tech-students-api-tests
тестовое на qa auto
стенд: http://93.77.188.34/apidocs
покрыл CRUD по /student
pytest + requests + allure

## Запуск
venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
в корне нужен .env:
```
BASE_URL=http://93.77.188.34
```

Запуск тестов:
```bash
pytest -n auto
```

Результаты Allure складываются в `allure-results`.

Отчёт:
```bash
allure serve allure-results
```
## Баги
Найденные баги API https://docs.google.com/spreadsheets/d/1PYdP2oZokkOvqkLIu3CehqCfOMiH-TAwvoPrN5y9I08/edit?usp=sharing
