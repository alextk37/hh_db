from datetime import datetime as dt
import os
import requests
import json


class HHVacanciesParser():
    """
    Класс для парсинга данных о вакансиях с сайта hh.ru.

    Методы:
    - __init__(): инициализирует экземпляр класса и
            определяет пути к файлам с данными о компаниях
    - get_urls(): извлекает URL-адреса вакансий из файлов с данными о компаниях
    - get_data(): получает данные о вакансиях по извлеченным URL-адресам
    - save_data(): сохраняет данные о вакансиях в файл

    """

    def __init__(self) -> None:
        self.employers_path = os.path.abspath('get_data/data_employers')
        self.employers_file = os.listdir(self.employers_path)[0]
        self.path = os.path.join(self.employers_path, self.employers_file)
        self.vacancies = []
        self.now = dt.now()

    def get_urls(self):
        with open(self.path,
                  'r',
                  encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            urls = []
            for chunk in json_data:
                urls.append(chunk.get('vacancies_url'))
            return urls

    def get_data(self):
        urls = self.get_urls()
        for url in urls:
            response = requests.get(url)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)

    def save_data(self):
        f = '%d-%m-%Y %H:%M:%S'
        abs_path = os.path.abspath('get_data/data_vacancies')
        if not os.listdir(abs_path):
            name = dt.strftime(self.now, f) + ' ' + 'vacancies' + ' ' + '.json'
            file_path = os.path.join(abs_path, name)
            self.get_data()
            with open(file_path, 'w') as json_file:
                json.dump(self.vacancies, json_file, ensure_ascii=False)
