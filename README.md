# Работа с базой данных PostgreSQL, компаниями/вакансиями hh.


## Описание:

Учебный проект


## Необходимое ПО:

1. PyCharm IDE (или другая)
2. poetry
3. git
4. pytest (Функциональность отстутствует)
5. pytest-cov (Функциональность отстутствует)
6. psycopg2-binary
7. requests
8. python-dotenv

## Для добавления библиотек:
poetry add psycopg2-binary
poetry add requests
poetry add python-dotenv

## Для добавления линтеров/форматтеров:

poetry add --group lint flake8
poetry add --group lint mypy
poetry add --group lint black
poetry add --group lint isort
poetry add --group dev pytest
poetry add --group dev pytest-cov


## Для тестирования функций:

1. Клонируйте репозиторий:
```
git clone git@github.com:andreylagunov/DB_Manager.git
```

2. Установите зависимости:

```
poetry install 
```

3. Для запуска тестирования инструментом pytest:

```
(Функциональность отстутствует)
pytest
```

4. Для формирования отчёта о покрытии тестами инструментом pytest-cov:

```
(Функциональность отстутствует)
pytest --cov=src --cov-report=html
```


## Описание работы функций:

### Модуль **api.py**
Содержит функциональность класса HeadHunterAPI.
Класс HeadHunterAPI имеет функционал:
```
def __init__(self):
    """Конструктор экземпляра обработчика запросов к hh."""
    
def get_dict_of_attributes(self) -> dict[str, str | dict | list]:
    """Служит для доступа на чтение к атрибутам экземпляра."""
    
def __check_connection(self) -> bool:
    """Отправляет запрос на базовый URL. Проверяет ответ."""
    
def is_connection_good(self) -> bool:
    """
    Обёртка над приватным методом подключения к API hh.
    Возвращает True, если запрос на базовый URL - успешен.
    """
```

### Модуль **user_interactions.py**
Содержит функции-обёртки, на базе которых происходит взаимодействие с пользователем.
Связывает в себе функции модулей api, data_base, vacancies


### Модуль **data_base.py**
Содержит функции создания БД, создания таблиц, проверки создания БД и таблиц.


### Модуль **vacancies.py**
Содержит функциональность класса DBManager. На базе этого класса пользователь обращается в БД.


### Модуль **main.py**
Связывает функциональности между собой,
отвечает за основную логику проекта и взаимодействие с пользователем.


### Пакет **tests**
Отстутствует в этом проекте

### Директория **data**
Отстутствует в этом проекте

### Директория **htmlcov**
Отстутствует в этом проекте

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).
