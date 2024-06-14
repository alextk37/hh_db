import json
from db_manager.db_manager import DBManager
from db_manager.config import emp_file, vac_file
from db_manager.get_db_config import config


class DBRequests():
    """
    Класс для выполнения запросов к базе данных.

    Атрибуты:
    - db (DBManager): экземпляр класса DBManager для
            управления подключением к базе данных

    Методы:
    - get_version(): возвращает версию базы данных
    - drop_table(): удаляет таблицы из базы данных
    - show_tables(): возвращает список таблиц в базе данных
    - create_tables(): создает таблицы в базе данных
    - filling_emp(): заполняет таблицу employers данными из файла
    - filling_vac(): заполняет таблицу vacancies данными из файла
    - get_companies_and_vacancies_count(): возвращает список компаний и
            количество вакансий
    - get_all_vacancies(): возвращает все вакансии
    - get_avg_salary(): возвращает среднюю зарплату
    - get_vacancies_with_higher_salary(): возвращает
            вакансии с зарплатой выше средней
    - get_vacancies_with_keyword(keyword): возвращает
            вакансии, содержащие ключевое слово

    """
    params = config()

    def __init__(self) -> None:
        '''
        Инициализирует экземпляр класса DBRequests.
        '''
        self.db = DBManager(**self.params)

    def get_version(self):
        '''
        Возвращает версию базы данных.
        '''
        prompt = 'SELECT version();'
        return self.db.req_resp(prompt)

    def drop_table(self):
        '''
        Удаляет таблицы 'vacancies' и 'employers' из базы данных.
        '''
        prompt = '''
                  DROP TABLE IF EXISTS public.vacancies;
                  DROP TABLE IF EXISTS public.employers;
                 '''
        self.db.req_not_resp(prompt)

    def show_tables(self):
        '''
        Возвращает список таблиц в базе данных.
        '''
        prompt = '''SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                 '''
        return self.db.req_resp(prompt)

    def create_tables(self):
        '''
        Создает таблицы 'employers' и 'vacancies' в базе данных.
        '''
        prompt = '''
                  CREATE TABLE employers (
                    id VARCHAR(255) NOT NULL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    open_vacancies INTEGER);

                  CREATE TABLE vacancies (
                    id VARCHAR(255) NOT NULL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    salary INT,
                    url VARCHAR(255) NOT NULL,
                    employer VARCHAR(255) NOT NULL,
                    description TEXT,
                  FOREIGN KEY (employer) REFERENCES employers(id));
                '''
        self.db.req_not_resp(prompt)

    def filling_emp(self):
        '''
        Заполняет таблицу 'employers' данными из JSON-файла.
        '''
        with open(emp_file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                prompt = f'''
                         INSERT INTO employers (id,
                                                name,
                                                description,
                                                open_vacancies)
                         VALUES ('{data.get('id')}',
                                 '{data.get('name')}',
                                 '{data.get('description')}',
                                 {data.get('open_vacancies')})
                        '''
                self.db.req_not_resp(prompt)

    def filling_vac(self):
        '''
        Заполняет таблицу 'vacancies' данными из JSON-файла
        '''
        with open(vac_file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            for data in json_data:
                if data['salary']:
                    if data['salary']['to']:
                        salary = int(data['salary']['to'])
                    elif data['salary']['from'] and not data['salary']['to']:
                        salary = int(data['salary']['from'])
                    else:
                        salary = 0
                else:
                    salary = 0
                prompt = f'''
                         INSERT INTO vacancies (id,
                                                name,
                                                salary,
                                                url,
                                                employer,
                                                description)
                         VALUES ('{data.get('id')}',
                                 '{data.get('name')}',
                                  {salary},
                                 '{data.get('alternate_url')}',
                                 '{data.get('employer')['id']}',
                                 '{data.get('snippet')['responsibility']}')
                          '''
                self.db.req_not_resp(prompt)

    def get_companies_and_vacancies_count(self):
        '''
        Возвращает названия компаний и количество открытых вакансий.
        '''
        prompt = '''SELECT name, open_vacancies
                    FROM employers
                    '''
        return self.db.req_resp(prompt)

    def get_all_vacancies(self):
        '''
        Возвращает все вакансии с информацией о компании,
        названии вакансии, зарплате и URL.
        '''
        prompt = '''SELECT e.name,
                           v.name,
                           v.salary,
                           v.url
                    FROM vacancies AS v
                    JOIN employers AS e
                    ON  v.employer = e.id
                    '''
        return self.db.req_resp(prompt)

    def get_avg_salary(self):
        '''
        Возвращает среднюю зарплату по всем вакансиям.
        '''
        prompt = '''SELECT ROUND(AVG(v.salary))
                    FROM vacancies AS v
                  '''
        return self.db.req_resp(prompt)

    def get_vacancies_with_higher_salary(self):
        '''
        Возвращает вакансии с зарплатой выше среднего значения.
        '''
        prompt = '''SELECT name, salary, url
                    FROM vacancies
                    WHERE salary > (SELECT AVG(salary) FROM vacancies);
                 '''
        return self.db.req_resp(prompt)

    def get_vacancies_with_keyword(self, keyword):
        '''
        Возвращает вакансии, содержащие ключевое слово в названии.

        Параметры:
          self (object): экземпляр класса.
          keyword (str): ключевое слово для поиска в названиях вакансий
        '''
        prompt = f'''SELECT name, salary, url
                     FROM vacancies
                     WHERE name LIKE '%{keyword}%';
                 '''
        return self.db.req_resp(prompt)
