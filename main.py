from src.head_hunter_api import HeadHunterAPI
from src.vacancy import Vacancy
from src.json_saver import JSONSaver
from src.utils import printing


def user_interaction():
    getting_storage_location = input('Изменить хранилище вакансий? да/нет(enter): ')
    if getting_storage_location == 'да':
        new_file = input("Введите название файла для хранения вакансий: ") + '.json'
        json_saver = JSONSaver(new_file)
    else:
        json_saver = JSONSaver()

    while True:
        hh_api = HeadHunterAPI()
        search_query = input("Введите поисковый запрос: ")
        print("Получаем вакансии. Ожидайте...")
        hh_vacancies = hh_api.get_vacancies(search_query)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

        choice_user = input('\nВыберите действие:\n'
                            '1. Отсортировать вакансии\n'
                            '2. Показать вакансии\n'
                            '3. Работа с хранилищем вакансий\n'
                            '4. Выход\n')
        if choice_user == '1':

            filtering_commands = input(f'\nСделать выборку по валюте, городу или зарплате?\n'
                                       f'1. да\n'
                                       f'2. нет\n')
            if filtering_commands == '1':
                user_commands = input('Выберите один или несколько фильтров через пробел:\n'
                                      '1. Город\n'
                                      '2. Зарплата\n'
                                      '3. Валюта\n').split()
                for command in user_commands:
                    if command == '1':
                        user_city = input('Введите город: ').lower()
                        vacancies_list = filter(lambda x: x.area.lower() == user_city, vacancies_list)
                    elif command == '2':
                        salary_range = int(input('Введите желаемую зарплату: '))
                        vacancies_list = filter(lambda x: int(x.salary['from']) >= salary_range, vacancies_list)
                    elif command == '3':
                        currency = dict()
                        key = 1
                        for vacancy in vacancies_list:
                            if vacancy.salary['currency'] not in currency.values():
                                currency[key] = vacancy.salary['currency']
                                key += 1

                        for key, value in currency.items():
                            print(f'{key}. {value}')
                        user_currency = int(input('Выберите валюту: '))
                        vacancies_list = filter(lambda x: x.salary['currency'] == currency[user_currency],
                                                vacancies_list)

            choice_input = input('\n1. Показать вакансии\n2. Вывести топ N вакансий по зарплате\n')

            if choice_input == '1':
                printing(vacancies_list)
            elif choice_input == '2':
                top_n = int(input('Введите количество вакансий для вывода в топ N: '))
                sorted_vacancies = sorted(vacancies_list, reverse=True)
                top_vacancies = sorted_vacancies[:top_n]
                printing(top_vacancies)

        elif choice_user == '2':
            printing(vacancies_list)
        elif choice_user == '3':
            file_action = input('1. Добавить найденные вакансии в хранилище\n'
                                '2. Удалить найденные вакансии из хранилища\n'
                                '3. Очистить хранилище\n'
                                '4. Выход\n')
            vacancies_list_dict = Vacancy.to_dict(vacancies_list)

            if file_action == '1':
                json_saver.add_vacancies(vacancies_list_dict)
            elif file_action == '2':
                json_saver.delete_vacancy(vacancies_list_dict)
            elif file_action == '3':
                json_saver.clear_file()
            elif file_action == '4':
                break
        elif choice_user == '4':
            break
        input_user = input('1. Продолжить поиск\n2. Выход\n')
        if input_user == '1':
            continue
        elif input_user == '2':
            break


if __name__ == "__main__":
    user_interaction()
