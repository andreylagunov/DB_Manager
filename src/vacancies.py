from psycopg2._psycopg import connection

from src.data_base import create_connection_with


class DBManager:
    """
    Класс для работы с вакансиями БД,
    подключается к Postgre БД (исп. библиотеку psycopg2)
    """

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Возвращает:  список всех компаний и количество вакансий у каждой компании.
        (использует SQL-запрос, выводящий информацию о вакансиях и компаниях через JOIN)
        """
        conn: connection = create_connection_with("project_3_db")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.employer_name, COUNT(*)
                FROM companies
                JOIN vacancies USING(employer_id)
                GROUP BY companies.employer_name;
            """
            )
            rows: list[tuple] = cur.fetchall()

        conn.close()
        return rows

    def get_all_vacancies(self) -> list[tuple]:
        """
        Возвращает:     список всех вакансий
                        с указанием:     названия компании, названия вакансии и зарплаты и ссылки на вакансию
        (использует SQL-запрос, выводящий информацию о вакансиях и компаниях через JOIN)
        """
        conn: connection = create_connection_with("project_3_db")
        with conn.cursor() as cur:
            cur.execute(
                """
SELECT companies.employer_name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
FROM companies
JOIN vacancies USING(employer_id);"""
            )
            rows: list[tuple] = cur.fetchall()
        conn.close()

        return rows

    def get_avg_salary(self) -> int:
        """
        Возвращает:     среднюю зарплату по всем вакансиям
        (использует SQL-запрос, выводящий информацию о средней зарплате через функцию AVG)
        """
        conn: connection = create_connection_with("project_3_db")
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_to + salary_from) / 2)
                FROM vacancies
                WHERE salary_from <> 0 AND salary_to <> 0;
            """
            )
            average_salary: list[tuple] = cur.fetchall()
        conn.close()

        return round(average_salary[0][0])

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Возвращает:     список всех вакансий, у которых зарплата выше средней по всем вакансиям
        (использует SQL-запрос, выводящий информацию о средней зарплате через фильтрацию WHERE)
        """
        # SELECT companies.employer_name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
        # FROM companies
        # JOIN vacancies
        # USING(employer_id);
        conn: connection = create_connection_with("project_3_db")
        with conn.cursor() as cur:
            cur.execute(
                """
SELECT companies.employer_name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
FROM companies
JOIN vacancies USING(employer_id)
WHERE salary_from > 0
AND salary_from > (SELECT AVG((salary_to + salary_from) / 2) FROM vacancies WHERE salary_from > 0 AND salary_to > 0);
            """
            )
# SELECT *
# FROM vacancies
# WHERE salary_from > 0
# AND salary_from > (SELECT AVG((salary_to + salary_from) / 2) FROM vacancies WHERE salary_from > 0 AND salary_to > 0);
            vacancies_with_higher_salary: list[tuple] = cur.fetchall()
        conn.close()

        return vacancies_with_higher_salary

    def get_vacancies_with_keyword(self, keywords: list[str]) -> list[tuple]:
        """
        Возвращает:     список всех вакансий, в названии которых содержатся переданные в метод слова
        (используется SQL-запрос, выводящий список всех вакансий,
        в названии которых содержатся переданные в метод слова через оператор LIKE)
        """
        # Формируем строку с WHERE      - фильтр запроса:
        where_query_str: str = "WHERE "
        for word in keywords:

            # Чтобы исключить "проблему с первой буквой" в названии вакансии,
            # первую букву искомого слова отбрасываем.
            where_query_str += f"vacancies.name LIKE '%{word.lower()[1:]}%'"

            # Если слово не конечное, добавляем соединение OR в запрос.
            if word != keywords[-1]:
                where_query_str += " OR "
            # Иначе добавляем ";" - окончание запроса
            else:
                where_query_str += ";"

        conn: connection = create_connection_with("project_3_db")
        with conn.cursor() as cur:
            cur.execute(
                f"""
SELECT companies.employer_name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url
FROM companies
JOIN vacancies USING(employer_id)
                {where_query_str}
            """
            )
            vacancies_with_keyword: list[tuple] = cur.fetchall()
        conn.close()

        return vacancies_with_keyword
