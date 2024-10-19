from abc import ABC, abstractmethod

import requests


class BaseClassAPI(ABC):

    @abstractmethod
    def _get_response(self):
        pass

    @abstractmethod
    def get_vacancies(self, search_query):
        pass


class HeadHunterAPI(BaseClassAPI):

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100, "only_with_salary": "true"}
        self.vacancies = []

    def _get_response(self):
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.status_code == 200:
            return response
        else:
            print(f"Ошибка при запросе к API. Код ошибки: {response.status_code}")

    def get_vacancies(self, keyword):
        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = self._get_response()
            vacancies = response.json()["items"]
            self.vacancies.extend(vacancies)
            self.__params["page"] += 1
            if response.json()["pages"] == self.__params["page"]:
                break
        return self.vacancies
