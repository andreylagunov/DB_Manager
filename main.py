from src.api import HeadHunterAPI
from src.vacancies import DBManager
from src.data_base import is_database_created
from src.data_base import drop_database
from src.user_interactions import user_selection_and_run
from src.user_interactions import vacancies_limit_question
from src.user_interactions import prefiltering_question
from src.user_interactions import db_creation
from src.user_interactions import db_tables_creation
from src.user_interactions import check_connection
from src.user_interactions import searching
from src.user_interactions import converting_and_insertion


def user_interaction() -> None:
    """
    Функция взаимодействия с пользователем
    """

    if is_database_created("project_3_db"):
        drop_database("project_3_db")

    # Вопрос пользователю по кол-ву вакансий, далее сохраняемых для одной компании.
    vacancies_limit: int = vacancies_limit_question()

    # Вопрос пользователю по предварительной фильтрации запрашиваемых с HH вакансий.
    filtering_words_str: str = prefiltering_question()

    # Создаём БД, проверка факта создания.
    is_db_created: bool = db_creation()
    if not is_db_created:
        return

    # Создаём таблицы компаний и вакансий, проверка факта создания.
    is_tables_created: bool = db_tables_creation()
    if not is_tables_created:
        return

    hh_handler: HeadHunterAPI = HeadHunterAPI()

    # Проверка соединения с API HeadHunter
    is_connection_good: bool = check_connection(hh_handler)
    if not is_connection_good:
        return

    # Настройка обращений к HH согласно предыдущим ответам пользователя.
    hh_handler.set_vacancies_limit(vacancies_limit)
    hh_handler.set_keywords_on_search(filtering_words_str)

    # Запрос на HH, преобразование информации в вид для БД, запись в таблицы БД.
    searching(hh_handler)
    converting_and_insertion(hh_handler)

    # Обработка основных запросов пользователя согласно функционалу класса DBManager.
    dbmanager = DBManager()
    user_selection_and_run(dbmanager)


if __name__ == "__main__":
    user_interaction()
