from src.api import HeadHunterAPI
from src.data_base import (create_companies_table, create_database,
                           create_vacancies_table, insert_into_table,
                           is_companies_table_exist, is_database_created,
                           is_vacancies_table_exist)
from src.vacancies import DBManager


def vacancies_limit_question() -> int:
    """
    Запрашивает у пользователя значие-предел кол-ва вакансий,
    хранящихся в БД в рамках одной компании.
    """
    user_input: str = ""
    print(
        """Здравствуйте.
    Сейчас будет создана база данных под хранение компаний и вакансий.
    Какое предельное кол-во вакансий будем хранить для одной компании?"""
    )
    while not user_input.isdigit():
        user_input = input("Введите целое число: ")
    vacancies_limit: int = int(user_input)
    print(f"Предельное кол-во вакансий установили в значение {vacancies_limit}.")
    return vacancies_limit


def prefiltering_question() -> str:
    """
    Запрашивает у пользователя слова, по которым с HH будут запрашиваться вакансии.
    Предфильтация первичная (вне запросов к ДБ).
    """
    print(
        """\nПод 10 заранее определённых компаний будем запрашивать с HeadHunter'a их вакансии.
    Если нужна на данном этапе фильтрация вакансий по желаемым словам, укажите их через пробел.
    Если не нужна - оставьте ввод пустым (и нажмите Enter)."""
    )
    words_str: str = input("Слова предварительной фильтрации: ")
    words_list: list[str] = words_str.split()
    if words_list:
        print("Для фильтрации установлены слова:")
        for word in words_list:
            print("                                 ", word)
    else:
        print("                                 Фильтрация не задана.")

    return words_str


def db_creation() -> bool:
    """
    Созданёт БД, проверяет факт создания.
    Возвращает True в случае успеха. Иначе - False.
    """
    print("\nСоздаём базу данных с именем project_3_db...")
    if not is_database_created("project_3_db"):
        create_database("project_3_db")
    print("Проверяем факт создания...")
    if is_database_created("project_3_db"):
        print("Создана успешно.")
        return True
    else:
        print("Что-то пошло не так. Завершение выполнения.")
        return False


def db_tables_creation() -> bool:
    """
    Созданёт таблицы в БД, проверяет факт создания.
    Возвращает True в случае успеха. Иначе - False.
    """
    print("\nСоздаём таблицы компаний и вакансий...")
    if not is_companies_table_exist():
        create_companies_table()
    if not is_vacancies_table_exist():
        create_vacancies_table()
    print("Проверяем факт создания...")
    if is_companies_table_exist() and is_vacancies_table_exist():
        print("Созданы успешно.")
        return True
    else:
        print("Что-то пошло не так. Завершение выполнения.")
        return False


def check_connection(hh_handler: HeadHunterAPI) -> bool:
    """
    Проверяет соединение с HH-ресурсом.
    Возвращает True в случае успеха. Иначе - False.
    """
    print("\nПроверка соединения с API HeadHunter...")
    if hh_handler.is_connection_good():
        print("С соединением всё хорошо.")
        return True
    else:
        print("С соединением проблемы. Завершение выполнения.")
        return False


def searching(hh_handler: HeadHunterAPI) -> None:
    """
    Обёртка над действием поиска.
    """
    print("Делаем запросы к HeadHunter по компаниям и их вакансиям...")
    hh_handler.search_raw_vacancies_from_companies()


def converting_and_insertion(hh_handler: HeadHunterAPI) -> None:
    """
    Обёртка над действиями преобразования информации из формы HH в форму тублиц БД.
    Включая запись в таблицы.
    """
    print("\nПреобразуем информацию вакансий для записи в базу данных...", end=" ")
    db_vacancies_list: list[dict] = hh_handler.convert_raw_vacancies__for_db()
    print(f"Получился список из {len(db_vacancies_list)} вакансий.")

    print("Создаём список компаний для записи в базу данных...", end=" ")
    db_companies_list: list[dict] = hh_handler.create_companies_list__for_db()
    print(f"Получился список из {len(db_companies_list)} компаний.")

    print("Записываем...")
    insert_into_table("companies", db_companies_list)
    insert_into_table("vacancies", db_vacancies_list)


def companies_and_vacancies_count(instance: DBManager) -> None:
    """
    Отрабатывает согласно методу    get_companies_and_vacancies_count   класса DBManager.
    Выводит человекочитаемые строки.
    """
    print("\nВыводим названия компаний с кол-вом их вакансий...")
    rows: list[tuple] = instance.get_companies_and_vacancies_count()
    for row in rows:
        print(f"{row[0]}:   {row[1]}")


def all_vacancies(instance: DBManager) -> None:
    """
    Отрабатывает согласно методу    get_all_vacancies   класса DBManager.
    Выводит человекочитаемые строки.
    """
    print("\nВыводим все доступные вакансии...")
    rows: list[tuple] = instance.get_all_vacancies()
    for row in rows:
        salary_from: str | int = "..."
        salary_to: str | int = "..."
        if row[2] != 0:
            salary_from = row[2]
        if row[3] != 0:
            salary_to = row[3]
        print(
            f"""{row[0]}, {row[1]},   ЗП: {salary_from} - {salary_to} руб,   {row[4]}"""
        )


def avg_salary(instance: DBManager) -> None:
    """
    Отрабатывает согласно методу    get_avg_salary   класса DBManager.
    Выводит человекочитаемые строки.
    """
    average_salary: int = instance.get_avg_salary()
    print(f"\nСредняя ЗП по вакансиям (у которых указана ЗП):   {average_salary} руб.")


def vacancies_with_higher_salary(instance: DBManager) -> None:
    """
    Отрабатывает согласно методу    get_vacancies_with_higher_salary   класса DBManager.
    Выводит человекочитаемые строки.
    """
    vacancies_with_higher_salary: list[tuple] = (
        instance.get_vacancies_with_higher_salary()
    )
    if len(vacancies_with_higher_salary):
        print("\nСписок вакансий, ЗП которых выше средней:\n")
        for vacancy in vacancies_with_higher_salary:
            salary_from: str | int = "..."
            salary_to: str | int = "..."
            if vacancy[2] != 0:
                salary_from = vacancy[2]
            if vacancy[3] != 0:
                salary_to = vacancy[3]
            print(
                f"""{vacancy[0]}, {vacancy[1]},   ЗП: {salary_from} - {salary_to} руб,   {vacancy[4]}"""
            )
    else:
        print("\nВакансий не найдено")


def vacancies_with_keyword(instance: DBManager, keywords_list: list[str]) -> None:
    """
    Отрабатывает согласно методу    get_vacancies_with_keyword   класса DBManager.
    Выводит человекочитаемые строки.
    """
    vacancies_with_keyword: list[tuple] = instance.get_vacancies_with_keyword(
        keywords_list
    )
    if len(vacancies_with_keyword):
        print("\nСписок вакансий по заданным ключевым словам:\n")
        for vacancy in vacancies_with_keyword:
            salary_from: str | int = "..."
            salary_to: str | int = "..."
            if vacancy[2] != 0:
                salary_from = vacancy[2]
            if vacancy[3] != 0:
                salary_to = vacancy[3]
            print(
                f"""{vacancy[0]}, {vacancy[1]},   ЗП: {salary_from} - {salary_to} руб,   {vacancy[4]}"""
            )
    else:
        print("\nВакансий не найдено")


def user_selection_and_run(db_manager_instance: DBManager) -> None:
    """
    Запрос у пользователя предпочитаемого действия
    (согласно возможностям класса DBManager)
    """

    while True:
        user_input = "0"
        while user_input not in "123456":
            user_input = input(
                """
Выберите действие, указав его номер:
1.  Вывести список всех компаний и количество вакансий у каждой компании.
2.  Вывести список всех вакансий с указанием названия компании, названия вакансии, ЗП, URL вакансии.
3.  Вывести среднюю ЗП по вакансиям.
4.  Вывести список всех вакансий, у которых ЗП выше средней по всем вакансиям.
5.  Вывести список всех вакансий, в названии которых содержатся указываемые слова (например python).
6.  Выход
"""
            )

        if user_input == "1":
            # Выводим перечень компания и кол-вом вакансий каждой.
            companies_and_vacancies_count(db_manager_instance)

        elif user_input == "2":
            # Выводим все вакансии из созданной БД.
            all_vacancies(db_manager_instance)

        elif user_input == "3":
            # Выводим среднюю ЗП из тех вакансий, для которых она указана.
            avg_salary(db_manager_instance)

        elif user_input == "4":
            # Выводим вакансии, ЗП которых выше средней.
            vacancies_with_higher_salary(db_manager_instance)

        elif user_input == "5":
            # Выводим вакансии с наличием в их названии указанных слов.
            keywords_list: list[str] = get_user_words()
            vacancies_with_keyword(db_manager_instance, keywords_list)

        else:
            return


def get_user_words() -> list[str]:
    """
    Запрашивает у пользователя слова для фильтрации.
    Возвращает список слов.
    """
    user_input: str = input(
        """\nВведите (разделённые пробелом) слова,
по которым отфильтруем вакансии, и нажмите Enter.\nСлова:   """
    )

    list_of_words: list[str] = user_input.split()
    if len(list_of_words) == 0:
        list_of_words = ["Программист", "Разработчик", "Python"]
        print(
            "Ваших слов в вводе не обнаружено. Установили слова по умолчанию:  Программист, Разработчик, Python"
        )
    else:
        print("Установили фильтрацию по словам:   ", end="")
        for word_ in list_of_words:
            if word_ != list_of_words[-1]:
                print(word_, end=", ")
            else:
                print(word_)

    return list_of_words
