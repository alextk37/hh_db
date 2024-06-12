import os

db_conf = {'dbname': 'postgres',
           'user': 'postgres',
           'password': 'secret',
           'host': 'localhost',
           'port': '5438'}

emp_path = os.path.abspath('get_data/data_employers')
emp_name = os.listdir(emp_path)[0]
emp_file = os.path.join(emp_path, emp_name)

vac_path = os.path.abspath('get_data/data_vacancies')
vac_name = os.listdir(vac_path)[0]
vac_file = os.path.join(vac_path, vac_name)
