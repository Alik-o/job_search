import re


class Vacancy:
    __slots__ = ["name", "url", "salary", "area", "description"]

    def __init__(self, name, url, salary, area, description):
        self.name = name
        self.url = url
        validated_salary = self.__salary_check(salary)
        self.salary = validated_salary
        self.area = area
        self.description = self.__correction_of_description(description)

    def __str__(self):
        if self.salary == "Зарплата не указана":
            return f"{self.name}\n{self.url}\n{self.description}\n{self.area}\n{self.salary}\n\n"
        return (
            f"{self.name}\n{self.url}\n{self.description}\n{self.area}\n"
            f"{self.salary['from']} - {self.salary['to']} {self.salary['currency']}\n\n"
        )

    def __repr__(self):
        return (
            f"'name': {self.name}, 'url': {self.url}, 'description': {self.description},"
            f"'area': {self.area}, 'salary': {self.salary}"
        )

    def __gt__(self, other):
        return self.salary["to"] > other.salary["to"]

    @classmethod
    def cast_to_object_list(cls, vacancies):
        return [
            cls(
                vacancy["name"],
                vacancy["alternate_url"],
                vacancy["salary"],
                vacancy["area"]["name"],
                vacancy["snippet"]["requirement"],
            )
            for vacancy in vacancies
        ]

    @staticmethod
    def to_dict(vacancies):
        list_vacancy = []
        for vacancy in vacancies:
            vacancy_dict = dict(
                {
                    "name": vacancy.name,
                    "url": vacancy.url,
                    "salary": vacancy.salary,
                    "area": vacancy.area,
                    "description": vacancy.description,
                }
            )
            if vacancy_dict["description"]:
                vacancy_dict["description"] = re.sub(r"</?highlighttext>", "", vacancy_dict["description"])
            list_vacancy.append(vacancy_dict)
        return list_vacancy

    @staticmethod
    def __salary_check(salary):
        validated_salary = "Зарплата не указана"
        if salary is not None:
            if salary["from"] is None:
                validated_salary = {"from": 0, "to": salary["to"], "currency": salary["currency"]}
            elif salary["to"] is None:
                validated_salary = {"from": salary["from"], "to": salary["from"], "currency": salary["currency"]}
            else:
                validated_salary = {"from": salary["from"], "to": salary["to"], "currency": salary["currency"]}
        return validated_salary

    @staticmethod
    def __correction_of_description(description):
        if description is None:
            return None
        return re.sub(r"</?highlighttext>", "", description)
