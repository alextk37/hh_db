from get_data.get_company import HHCompanyParser, cleaner
from get_data.company_config import company_key as keys
from get_data.get_vacancies import HHVacanciesParser
from db_manager.db_requests import DBRequests
import os

emp_path = os.path.abspath('get_data/data_employers')
if os.listdir(emp_path):
    cleaner()
company_search = HHCompanyParser(keys)
if isinstance(company_search, HHCompanyParser):
    print('Локальные данные не обнаружены.')
    print('Загружаю информацию по компаниям из "company_config"')
    print('\n')
    company_search.save_data()
    vacancies = HHVacanciesParser()
    vacancies.save_data()

print('Пишу в базу данных')
req = DBRequests()
req.drop_table()
req.create_tables()
req.filling_emp()
req.filling_vac()
print('Можно начинать работать...')
print('\n')


print('1 - список компаний и количество вакансий у каждой.')
print('2 - все вакансии')
print('3 - средняя зарплата по вакансиям')
print('4 - вакансии, с зарплатой выше средней по всем вакансиям')
print('5 - поиск по ключевому слову')
print('6 - удалить локальные данные')

user_input = int(input())
match user_input:
    case 1:
        for employer in req.get_companies_and_vacancies_count():
            print(f'Работодатель: {employer[0]} - {employer[1]} вак.')
    case 2:
        for vac in req.get_all_vacancies():
            print(vac[1])
            print(f'Компания - {vac[0]}')
            if vac[2] == 0:
                print('Отсутствуют данные о зарплате')
            else:
                print(f'Зарплата - {vac[2]}')
            print(f'Ссылка на вакансию - {vac[3]}')
            print('\n')
    case 3:
        avg = req.get_avg_salary()[0][0]
        print(f'Средняя зарплата по вакансиям - {avg} руб.')
    case 4:
        for vac in req.get_vacancies_with_higher_salary():
            print(vac[0])
            print(f'Зарплата - {vac[1]}')
            print(f'Ссылка на вакансию - {vac[2]}')
            print('\n')
    case 5:
        keyword = input('Введите слово для поиска ->  ')
        for vac in req.get_vacancies_with_keyword(keyword):
            print(vac[0])
            if vac[1] == 0:
                print('Отсутствуют данные о зарплате')
            else:
                print(f'Зарплата - {vac[1]}')
            print(f'Ссылка на вакансию - {vac[2]}')
            print('\n')
    case 6:
        cleaner()
