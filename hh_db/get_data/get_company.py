from datetime import datetime as dt
import os
import requests
import json


class HHCompanyParser():
    """
    Класс для парсинга данных о компаниях с сайта hh.ru.

    Атрибуты:
    - abs_path (str): абсолютный путь к каталогу для
            сохранения данных о компаниях

    Методы:
    - __init__(keywords): инициализирует экземпляр
            класса с ключевыми словами для поиска
    - __find_id(): находит и сохраняет идентификаторы компаний
    - save_data(): сохраняет данные о компаниях в файл

    """

    abs_path = os.path.abspath('get_data/data_employers')

    def __new__(cls,  *args, **kwargs):
        if not os.listdir(cls.abs_path):
            return super().__new__(cls)

    def __init__(self, keywords) -> None:
        self.search_url = 'https://api.hh.ru/employers'
        self.keywords = keywords
        self.params = {'text': '',
                       'only_with_vacancies': 'true'}
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.__employers_id = []
        self.employers = []
        self.now = dt.now()

    def __find_id(self):
        for key in self.keywords:
            self.params['text'] = key
            response = requests.get(self.search_url,
                                    headers=self.headers,
                                    params=self.params)
            id = response.json()['items'][0]['id']
            self.__employers_id.append(id)

    def save_data(self):
        self.__find_id()
        for id in self.__employers_id:
            url = self.search_url + '/' + str(id)
            response = requests.get(url)
            employer = response.json()
            self.employers.append(employer)

        f = '%d-%m-%Y %H:%M:%S'
        name = dt.strftime(self.now, f) + ' ' + 'search' + ' ' + '.json'

        file_path = os.path.join(self.abs_path, name)
        with open(file_path, 'w') as json_file:
            json.dump(self.employers, json_file, ensure_ascii=False)


def cleaner():
    emp_path = os.path.abspath('get_data/data_employers')
    vac_path = os.path.abspath('get_data/data_vacancies')
    ls_emp = os.listdir(emp_path)
    ls_vac = os.listdir(vac_path)

    for name in ls_emp:
        file_path = os.path.join(emp_path, name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for name in ls_vac:
        file_path = os.path.join(vac_path, name)
        if os.path.isfile(file_path):
            os.remove(file_path)
