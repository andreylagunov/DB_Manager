import psycopg2
from psycopg2 import OperationalError
from psycopg2._psycopg import connection


def create_connection_with(db_name: str) -> connection:
    """
    Принимает название базы данных, с которой необходимо установить соединение.
    Возвращает объект соединения.
    """
    return psycopg2.connect(
        host="localhost", database=db_name, user="postgres", password="1234"
    )


def create_database(db_name: str) -> None:
    """
    Код автоматического создания БД.
    (вызывается в основном скрипте программы)
    """
    conn: connection = create_connection_with("postgres")

    cur = conn.cursor()
    conn.autocommit = True
    cur.execute(f"CREATE DATABASE {db_name};")
    # Закрытие курсора и соединения:
    cur.close()
    conn.close()


def is_database_created(db_name: str) -> bool:
    """
    Принимает имя базы данных.
    Возвращает True - если база данных распознаётся (т.е. создана). Иначе - False.
    """
    try:
        conn: connection = create_connection_with(db_name)
        conn.close()
    except OperationalError:
        return False
    return True


def create_companies_table() -> None:
    """
    Код автоматического создания таблицы.
    (вызывается в основном скрипте программы)
    """
    conn: connection = create_connection_with("project_3_db")

    cur = conn.cursor()
    conn.autocommit = True
    cur.execute(
        """
        CREATE TABLE companies
        (
            employer_id int PRIMARY KEY,
            employer_name varchar(100) NOT NULL,
            employer_url varchar(100) NOT NULL
        );"""
    )
    # Закрытие курсора и соединения:
    cur.close()
    conn.close()


def is_table_exist(db_name: str, table_name: str) -> bool:
    """
    Принимает названия базы данных и таблицу, существование которой необходимо проверить.
    Возвращает True - если таблица существует. Иначе - False.
    """
    conn: connection = create_connection_with(db_name)

    cur = conn.cursor()
    conn.autocommit = True
    try:
        cur.execute(f"""SELECT * FROM {table_name};""")
    except psycopg2.Error:
        return False
    # Закрытие курсора и соединения:
    cur.close()
    conn.close()
    return True


def is_companies_table_exist() -> bool:
    """Проверяет существование таблицы компаний."""
    return is_table_exist("project_3_db", "companies")


def is_vacancies_table_exist() -> bool:
    """Проверяет существование таблицы вакансий."""
    return is_table_exist("project_3_db", "vacancies")


def create_vacancies_table() -> None:
    """
    Код автоматического создания таблицы.
    (вызывается в основном скрипте программы)
    """
    conn: connection = create_connection_with("project_3_db")

    cur = conn.cursor()
    conn.autocommit = True
    cur.execute(
        """
        CREATE TABLE vacancies
        (
            employer_id int,
            id serial PRIMARY KEY,
            name varchar(100) NOT NULL,
            salary_from int,
            salary_to int,
            snippet_requirement varchar(500) NOT NULL,
            url varchar(100) NOT NULL
        );
        """
    )
    cur.execute(
        "ALTER TABLE vacancies ADD FOREIGN KEY (employer_id) REFERENCES companies(employer_id);"
    )
    # Закрытие курсора и соединения:
    cur.close()
    conn.close()


def drop_database(db_name: str) -> None:
    """
    Принимает название базы данных.
    Удаляет эту базу.
    """
    conn: connection = create_connection_with("postgres")

    cur = conn.cursor()
    conn.autocommit = True
    cur.execute(f"DROP DATABASE {db_name};")
    # Закрытие курсора и соединения:
    cur.close()
    conn.close()


def insert_into_table(table_name: str, data_list: list[dict]) -> None:
    """
    Заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
    """
    conn: connection = create_connection_with("project_3_db")
    with conn.cursor() as cur:

        if table_name == "companies":
            for dict_ in data_list:
                cur.execute(
                    f"""
                INSERT INTO companies (employer_id, employer_name, employer_url)
                VALUES ({dict_["employer_id"]}, '{dict_["employer_name"]}', '{dict_["employer_url"]}');
                """
                )
                conn.commit()

        elif table_name == "vacancies":
            for dict_ in data_list:
                cur.execute(
                    f"""
                        INSERT INTO vacancies (employer_id, name, salary_from, salary_to, snippet_requirement, url)
                        VALUES (
                            {dict_["employer_id"]},
                            '{dict_["name"]}',
                            '{dict_["salary_from"]}',
                            '{dict_["salary_to"]}',
                            '{dict_["snippet_requirement"]}',
                            '{dict_["url"]}');
                    """
                )
                conn.commit()
    conn.close()


if __name__ == "__main__":
    companies_test_data: list[dict] = [
        {
            "employer_id": 400500,
            "employer_name": "СБЕР",
            "employer_url": "hh.employer.1",
        },
        {
            "employer_id": 400501,
            "employer_name": "Т-Банк",
            "employer_url": "hh.employer.2",
        },
    ]
    vacancies_test_data: list[dict] = [
        {
            "employer_id": 400500,
            "id": 5,
            "name": "C++ Разработчик",
            "salary_from": 100000,
            "salary_to": 160000,
            "snippet_requirement": "C/C++",
            "url": "hh1",
        },
        {
            "employer_id": 400501,
            "id": 6,
            "name": "Java Разработчик",
            "salary_from": 90000,
            "salary_to": 140000,
            "snippet_requirement": "Java SQL git",
            "url": "hh2",
        },
    ]

    # drop_database("project_3_db")

    # create_database("project_3_db")

    # create_companies_table()
    # print(is_table_exist("project_3_db", "companies"))

    # create_vacancies_table()
    # print(is_table_exist("project_3_db", "vacancies"))

    # insert_into_table("companies", companies_test_data)
    # insert_into_table("vacancies", vacancies_test_data)

    # try:
    #     insert_into_table("companies", companies_test_data)
    #     print("Успешное добавление данных в таблицу companies.")
    # except OperationalError as err:
    #     print("Что то пошло не так...", err)

    # print(is_database_created("project_3_db"))
    # print(is_database_created("project_3"))
    # print(is_database_created("test"))
    # print(is_database_created("postgres"))

    # conn: connection = create_connection_with("project_3_db")
    #
    # cur = conn.cursor()
    # conn.autocommit = True
    # try:
    #     cur.execute(f"""SELECT * FROM companies;""")
    # except psycopg2.Error as err:
    #     print("Ошибка...", err)
    # # Закрытие курсора и соединения:
    # cur.close()
    # conn.close()
    # print("Конец выполнения.")
