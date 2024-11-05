from pprint import pprint

import requests


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        """Конструктор экземпляра обработчика запросов к hh."""

        # self.__url = "https://api.hh.ru/employers"
        self.__url: str = "https://api.hh.ru/vacancies"
        # self.__headers = {"User-Agent": "HH-User-Agent"}
        # self.__params = {"text": "", "page": 0, "per_page": 500}
        self.__vacancies_limit: int = 10
        self.__keywords_str: str = "Python Разработчик"
        self.__company_name___vacancies_list: dict = {}
        self.__raw_vacancies_list: list = []
        self.__companies: list[dict[str, str | int]] = [
            {"comp_name": "T-Банк", "comp_id": 78638},
            {"comp_name": "СБЕР", "comp_id": 3529},
            {"comp_name": "Альфа-Банк", "comp_id": 80},
            {"comp_name": "KAMAZ DIGITAL", "comp_id": 5566914},
            {"comp_name": "ООО Автотех", "comp_id": 5267014},
            {"comp_name": "ООО Эвокарго", "comp_id": 4751605},
            {"comp_name": "Яндекс", "comp_id": 1740},
            {"comp_name": "ООО Гумич РТК", "comp_id": 3875659},
            {"comp_name": "idaproject", "comp_id": 1579449},
            {"comp_name": "Ozon Информационные технологии", "comp_id": 2180},
        ]
        self.user_companies_list: list[str] = [
            dict_["comp_name"] for dict_ in self.__companies
        ]

    #
    # def get_dict_of_attributes(self) -> dict[str, str | dict | list]:
    #     """Служит для доступа на чтение к атрибутам экземпляра."""
    #
    #     return {"url": self.__url, "headers": self.__headers, "params": self.__params, "vacancies": self.vacancies}

    def __check_connection(self) -> bool:
        """Отправляет запрос на базовый URL. Проверяет ответ."""

        response = requests.get(self.__url)
        code: int = response.status_code
        # print(f"__check_connection:  Статус код - {code}")
        if code == 200:
            return True
        return False

    def is_connection_good(self) -> bool:
        """
        Обёртка над приватным методом подключения к API hh.
        Возвращает True, если запрос на базовый URL - успешен.
        """
        return self.__check_connection()

    # def get_vacancies_data(self, keyword: str, per_page: int, to_page: int) -> None:
    #     """
    #     Принимает:  ключевое слово для поиска вакансий,
    #     Формирует параметры для запроса из 'text', 'per_page',
    #     Отправляет запрос для получения данных о вакансиях по ключ.слову.
    #     """
    #     # На каждый вызов функции - очистка списка вакансий.
    #     self.vacancies = []
    #
    #     self.__params["text"] = keyword
    #     self.__params["per_page"] = per_page
    #     if self.__check_connection():
    #         while self.__params.get("page") != to_page:
    #             response = requests.get(self.__url, headers=self.__headers, params=self.__params)
    #             vacancies = response.json()["items"]
    #             self.vacancies.extend(vacancies)
    #             self.__params["page"] += 1
    #         self.__params["page"] = 0

    # def get_company_data(self, company_name: str, per_page: int, to_page: int) -> None:

    # def get_company_data(self, company_name: str) -> None:
    #     """
    #     Принимает:  ключевое слово для поиска компании,
    #     Формирует параметры для запроса из 'text', 'per_page',
    #     Отправляет запрос для получения данных о вакансиях по ключ.слову.
    #     """
    #     # На каждый вызов функции - очистка списка вакансий.
    #     self.companies = []
    #
    #     self.__params["text"] = company_name
    #     self.__params["per_page"] = 50
    #     if self.__check_connection():
    #         # while self.__params.get("page") != to_page:
    #         response = requests.get(self.__url, headers=self.__headers, params=self.__params)
    #         company_data = response.json()["items"]
    #         self.companies.extend(company_data)
    #         # self.__params["page"] += 1
    #         # self.__params["page"] = 0

    def set_vacancies_limit(self, vacancies_limit: int) -> None:
        """
        Принимает значение - предел кол-ва вакансий поиска.
        Устанавливает ограничение на кол-во искомых вакансий.
        """
        self.__vacancies_limit = vacancies_limit

    def set_keywords_on_search(self, keywords: str) -> None:
        """
        Принимает:  список слов для фильтрации искомых вакансий.
        Устанавливает данный список как параметр обработчика запросов.
        """
        self.__keywords_str = keywords

    def search_raw_vacancies_from_companies(self) -> None:
        """
        Делает запрос на HH для получения вакансий по списку работодателей.
        формирует промежуточный словарь вида { "СБЕР": vacancies_list,      "Яндекс": vacancies_list,    ...}
        """
        for comp_dict in self.__companies:

            params: dict[str, str | int] = {
                "employer_id": comp_dict["comp_id"],
                "text": self.__keywords_str,
                "page": 0,
                "per_page": self.__vacancies_limit,  # макс. кол-во вакансий в выдаче запроса
            }

            response = requests.get("https://api.hh.ru/vacancies", params=params)
            vacancies_list: list[dict] = response.json()["items"]
            # data: dict = response.json()

            # Из каждого ответа response.json()
            # формируем промежуточный словарь вида { "СБЕР": vacancies_list,      "Яндекс": vacancies_list,    ...}
            self.__company_name___vacancies_list[comp_dict["comp_name"]] = (
                vacancies_list
            )

            # Можно "писать" сырые вакансии одним списком без привязки к компании.
            vacancies_from_company: list[dict] = response.json()["items"]
            self.__raw_vacancies_list.extend(vacancies_from_company)

    def raw_vacancies_list(self) -> list[dict]:
        """
        Возвращает список "необработанных сырых" вакансий.
        """
        return self.__raw_vacancies_list

    def raw_vacancies_dict___by_company(self) -> dict[str, list]:
        """
        Возвращает словарь с "сырыми" вакансиями вида { "СБЕР": vacancies_list,      "Яндекс": vacancies_list,    ...}
        """
        return self.__company_name___vacancies_list

    def convert_raw_vacancies__for_db(self) -> list[dict]:
        """
        Преобразует полученный с HeadHunter'a 'сырой' список вакансий     в список вакансий под формат таблицы БД,
        который будет записываться далее в таблицу вакансий Базы Данных.
        """
        list_of_dicts__for_db: list[dict] = []

        for dict_ in self.raw_vacancies_list():

            employer_id: int = dict_["employer"]["id"]
            name: str = dict_["name"]

            salary_from: int = 0
            salary_to: int = 0
            if type(dict_["salary"]) is dict:
                if type(dict_["salary"]["from"]) is int:
                    salary_from = dict_["salary"]["from"]
                if type(dict_["salary"]["to"]) is int:
                    salary_to = dict_["salary"]["to"]

            req: str = "Не указаны"
            if type(dict_["snippet"]) is dict:
                if type(dict_["snippet"]["requirement"]) is str:
                    req = dict_["snippet"]["requirement"]
            quotation_mark_free_str: str = req.replace("'", "")

            url: str = dict_["url"]

            db_vacancy_dict: dict[str, str | int] = {
                "employer_id": employer_id,
                # "id": 0,
                "name": name,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "snippet_requirement": quotation_mark_free_str,
                "url": url,
            }

            list_of_dicts__for_db.append(db_vacancy_dict)

        return list_of_dicts__for_db

    # def delete_quotation_marks(self, requirements_str: str) -> str:
    #     """
    #     Вспомогательная функция.
    #     Удаляет в принимаемой строке символы одинарной кавычки.
    #     Используется в  convert_raw_vacancies__for_db
    #     """
    #     new_str: str = requirements_str.replace("'", "")
    #     return new_str

    def create_companies_list__for_db(self) -> list[dict]:
        """
        На основании начальной информации по компаниям, создаётся список словарей для БД вида:
        [{"employer_id": 700900, "employer_name": "СБЕР", "employer_url": "hh.ru/employer/700900"}, {}, ...]
        """
        companies_list__for_db: list[dict] = []

        for dict_ in self.__companies:
            company_dict: dict = {
                "employer_id": dict_["comp_id"],
                "employer_name": dict_["comp_name"],
                # "employer_url": self.__company_name___vacancies_list[dict_["comp_name"]][0]["employer"]["url"]
                "employer_url": f"https://api.hh.ru/employer/{dict_["comp_id"]}",
            }
            companies_list__for_db.append(company_dict)

        return companies_list__for_db

    # Формируем данные работодателя:
    # comp_id: int = 3529     # для СБЕР
    # comp_name: str = data["items"][0]["employer"]["name"]
    # comp_url: str = data["items"][0]["employer"]["url"]
    #
    #
    # # Формируем данные вакансии:
    # vacancy_comp_id: int = 3529     # для СБЕР
    # vacancy_id: int = 1     # формируется автоматически базой PostgreSQL
    # vacancy_url: str = data["items"][0]["url"]
    # vacancy_name: str = data["items"][0]["name"]
    # salary_from: int | None = data["items"][0]["salary"]["from"]
    # salary_to: int | None = data["items"][0]["salary"]["to"]
    # vacancy_requirement: str = data["items"][0]["snippet"]["requirement"]


if __name__ == "__main__":

    hh_handler: HeadHunterAPI = HeadHunterAPI()
    hh_handler.set_vacancies_limit(10)
    hh_handler.set_keywords_on_search("разработчик")
    hh_handler.search_raw_vacancies_from_companies()

    list_data: list = hh_handler.raw_vacancies_list()
    dict_data: dict = hh_handler.raw_vacancies_dict___by_company()

    print("Тип list_data:  ", type(list_data))
    print("Длина:  ", len(list_data))

    print("Тип dict_data:  ", type(dict_data))
    print("Длина:  ", len(dict_data))
    for key, value in dict_data.items():
        print(
            f"{key}:      Длина значения {len(value)}     Тип значения: {type(value)}"
        )
    # print("Тип значения:  ", type(dict_data["СБЕР"]))
    # print("Длина значения:  ", len(dict_data["СБЕР"]))

    pprint(dict_data["СБЕР"][0])

    # Данные работодателя:
    # response = requests.get("https://api.hh.ru/employers", params={"employer_id": companies_list[3]["comp_id"]})

    # Вакансии работодателя:
    # response = requests.get("https://api.hh.ru/vacancies", params=params)
    # data = response.json()
