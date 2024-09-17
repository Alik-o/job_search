import json
import os
from abc import ABC, abstractmethod

from config import DATA_DIR


class BaseSaver(ABC):

    @abstractmethod
    def add_vacancies(self, vacancies):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancies):
        pass

    @abstractmethod
    def reading_fail(self):
        pass


class JSONSaver(BaseSaver):

    def __init__(self, file="vacancies.json"):
        self.__file = file
        self.file_path = os.path.join(DATA_DIR, self.__file)
        self.check_dir()

    def add_vacancies(self, vacancies):
        if os.path.getsize(self.file_path) > 0:
            data_vacancies = self.reading_fail()
            data_vacancies.extend(vacancies)
        else:
            data_vacancies = vacancies
        edited_data = list({vacancy["url"]: vacancy for vacancy in data_vacancies}.values())

        self.overwriting_file(edited_data)

    def delete_vacancy(self, vacancies):
        try:
            data_vacancies = self.reading_fail()
        except Exception:
            data_vacancies = []
        data_dict = {vacancy["url"]: vacancy for vacancy in data_vacancies}
        for vacancy in vacancies:
            if vacancy["url"] in data_dict:
                data_dict.pop(vacancy["url"])
        edited_data = list(data_dict.values())
        self.overwriting_file(edited_data)

    def check_dir(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self.clear_file()

    def reading_fail(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            data_vacancies = json.load(file)
            return data_vacancies

    def overwriting_file(self, vacancies):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def clear_file(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("")
