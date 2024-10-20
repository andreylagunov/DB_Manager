# Работа с базой данных PostgeSQL, компаниями/вакансиями hh.


## Описание:

Учебный проект


## Необходимое ПО:

1. PyCharm IDE (или другая)
2. poetry
3. git
4. pytest
5. pytest-cov
6. psycopg2-binary
7. requests

## Для добавления библиотек:
poetry add psycopg2-binary
poetry add requests

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
pytest
```

4. Для формирования отчёта о покрытии тестами инструментом pytest-cov:

```
pytest --cov=src --cov-report=html
```


## Описание работы функций:

### Модуль **api.py**
Предоставляет абстрактный класс ConnectionByAPI и наследуемый от него HeadHunterAPI.
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
    
def get_vacancies_data(self, keyword: str, per_page: int, to_page: int) -> None:
    """
    Принимает:  ключевое слово для поиска вакансий,
    Формирует параметры для запроса из 'text', 'per_page',
    Отправляет запрос для получения данных о вакансиях по ключ.слову.
    """


```

### Модуль **file.py**
Предоставляет абстрактный класс FileHandler и наследуемый от него JSONHandler.
Класс JSONHandler имеет функционал:
```
def __init__(self, file_name: str = "default_vacancies_file.json"):
    """
    Конструктор экземпляра обработчика json-файла.
    В экземпляре есть атрибут - имя файла,
    которое может быть назначено при создании экземпляра.
    """  
    
def get_dict_of_attributes(self) -> dict[str, str]:
    """Возвращает словарь со значениями атрибутов экземпляра."""

def __create_file_if_needed(self) -> None:
    """Создание файла для хранения вакансий, если его не существует"""

def __read_file(self) -> list[dict]:
    """Чтение json-файла. Возврат списка словарей с вакансиями."""
    
def __write_file(self, vacancy_list: list) -> None:
    """Запись в json-файл списка вакансий."""

def get_data_from_file(self) -> list[dict]:
    """Возвращает список данных (вакансий) из файла."""

def add_data_to_file(self, vacancy: Vacancy) -> None:
    """
    Метод добавления данных в файл.
    В JSON-файл сохраняются (добавляются) данные (атрибуты класса Vacancy) списком словарей.
    """
    
def delete_data_from_file(self, vacancy: Vacancy) -> None:
    """Метод удаления данных (вакансии) из файла."""
```

### Модуль **vacancy.py**
Предоставляет класс Vacancy. Служит для представления вакансии в виде пяти свойств.
Для экономии памяти использует __slots__:

```
__slots__ = ("speciality", "requirements", "salary_str", "salary_dict", "https_path")


@classmethod
def __get_salary_str___from_dict(cls, vac: dict) -> str:
    """
    Принимает словарь-вакансию (с HeadHunter)
    Возвращает атрибут salary_str вида "От 100000 до 140000 RUR" для объекта Vacancy
    """
    
@classmethod
def test__get_salary_str___from_dict(cls, vac: dict) -> str:
    """Вспомогательный метод для тестирования."""
        
@classmethod
def __get_salary_dict___from_dict(cls, vac: dict) -> dict[str, int | str]:
    """
    Принимает словарь-вакансию (с HeadHunter)
    Возвращает атрибут salary_dict вида {"from": 100_000, "to": 140_000, "currency": "RUR"} для объекта Vacancy
    """
    
@classmethod
def test__get_salary_dict___from_dict(cls, vac: dict) -> dict:
    """Вспомогательный метод для тестирования."""
        
@classmethod
def cast_to___objects_list(cls, vacancies_list: list[dict]) -> list:
    """
    Преобразование из списка со словарями   (с ключами "name", "snippet"/"requirement", "salary", "url")
    в список объектов типа Vacancy.
    """
    
def __is_speciality_valid(self, value: Any) -> bool:
    """Проверка типа для атрибута speciality."""

def __is_requirements_valid(self, value: Any) -> bool:
    """Проверка типа для атрибута requirements."""

def __is_salary_dict_valid(self, salary_dict: Any) -> bool:
    """Проверка типа для атрибута salary_dict."""
    
def __is_salary_str_valid(self, value: Any) -> bool:
    """Проверка типа для атрибута salary_str."""

def __is_https_path_valid(self, value: Any) -> bool:
    """Проверка типа для атрибута https_path."""

def __init__(
    self, speciality: str, requirements: str, salary_str: str, salary_dict: dict[str, int | str], https_path: str
):
    """Конструктор экземпляра класса Vacancy"""
    
def __avrg_salaries(self, other) -> tuple[float]:
    """
    Общий метод для сравнения зарплат по их среднему значению.
    Возвращает средние ЗП двух объектов.
    """
    
def __eq__(self, other) -> bool:
    """Метод сравнения зарплат: равны ли."""

def __ne__(self, other) -> bool:
    """Метод сравнения зарплат: неравны ли."""

def __lt__(self, other) -> bool:
    """Метод сравнения зарплат: меньше ли."""
    
def __gt__(self, other) -> bool:
    """Метод сравнения зарплат: больше ли."""

def __ge__(self, other) -> bool:
    """Метод сравнения зарплат: равны ли или больше."""

def __le__(self, other) -> bool:
    """Метод сравнения зарплат: равны ли или меньше."""

def __str__(self) -> str:
    """Метод вывода информации (атрибутов экземпляра) для пользователя."""  
```

### Модуль **other.py**
Предоставляет вспомогательные функции для взаимодействия с пользователем, фильтрации вакансий, сортировки.
```
def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем.
    Запрашивает:
    - поисковый запрос,
    - кол-во (топ-N) вакансий по заработной плате для вывода,
    - ключевые слова в описании (для фильтрации),
    - диапазон зарплат для фильтрации.
    """
    
def final_save_vacancies_to_file(vacancies_obj_list: list[Vacancy]) -> None:
    """
    Принимает список объектов-вакансий.
    Запрашивает у пользователя подтверждение на сохранение в файл.
    Производит сохранение вакансий в файл (без дублирования в файле).

    """
    
def print_vacancies(vacancies_obj_list: list[Vacancy]) -> None:
    """
    Принимает список объектов типа Vacancy,
    Выводит в консоль объекты-вакансии в виде:
    Разработчик Python.   https...   От 60000 руб.   Знание Python (средний уровень). Знание ООП...
    (добавляет пробелы, точки)
    """

def get_top_vacancies(vacancies_obj_list: list[Vacancy], top_n: int) -> list[Vacancy]:
    """
    Принимает список объектов типа Vacancy,
    Возвращает список объектов-вакансий, длиной равный значению top-n.
    """

def sort_vacancies_by_magic_methods_inplace(vacancies_obj_list: list[Vacancy]) -> list[Vacancy]:
    """
    Принимает список объектов типа Vacancy,
    Возвращает отсортированный по зарплате (по убыванию) список объектов.
    """
    
def get_vacancies_by_salary(vacancies_obj_list: list[Vacancy], salary_dict: dict[str, int | str]) -> list[Vacancy]:
    """
    Принимает список объектов типа Vacancy, словарь с диапазоном зарплаты.
    Возвращает список объектов, у которых зарплата "пересекается" с указанным диапазоном.
    """

def filter_vacancies(vacancies_obj_list: list[Vacancy], filter_words: list[str]) -> list[Vacancy]:
    """
    Принимает список объектов типа Vacancy, список слов - для фильтрации списка объектов.
    Возвращает список объектов, в описании которых есть данные слова.
    """
    
def get_salary_range_from_user(currency: str = "RUR", is_in_test: bool = False) -> dict[str, int | str]:
    """
    Запрашивает у пользователя диапазон зарплат,
    Проверяет корректность диапазона.
    Возвращает словарь вида:     {"from": 50000, "to": 90000, "currency": "RUR"}
    """
```

### Модуль **main.py**

```
    """
    Связывает функциональности между собой,
    отвечает за основную логику проекта и взаимодействие с пользователем.
    """
```

### Пакет **tests**
Содержит тестовые модули для модулей api.py, file.py, vacancy.py, other.py

### Директория **data**
Служит для сохранения JSON-файлов.

### Директория **htmlcov**
Содержит информацию о покрытии тестами.

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).
