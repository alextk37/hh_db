import psycopg2


class DBManager:
    """
        Класс для управления подключением к базе данных (Singleton).

        Атрибуты:
        - dbname (str): имя базы данных
        - user (str): имя пользователя
        - password (str): пароль
        - host (str): хост (по умолчанию 'localhost')
        - port (int): порт

        Методы:
        - connect(): устанавливает соединение с базой данных
        - close(): закрывает соединение с базой данных
        - req_resp(prompt): выполняет SQL-запрос, возвращающий результат
                (например, SELECT-запрос)
        - req_not_resp(prompt): выполняет SQL-запрос, не возвращающий
                результат (например, INSERT, UPDATE, DELETE-запросы)
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        DBManager.__instance = None

    def __init__(self, dbname, user, password, port, host='localhost'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def close(self):
        try:
            self.conn.close()
        except AttributeError:
            print('Ошибка подключения к БД')

    def req_resp(self, prompt):
        try:
            self.connect()
            self.cursor.execute(prompt)
            return self.cursor.fetchall()
        except AttributeError:
            print('Ошибка подключения к БД')
        finally:
            self.close()

    def req_not_resp(self, prompt):
        try:
            self.connect()
            self.cursor.execute(prompt)
        except AttributeError:
            print('Ошибка подключения к БД')
        finally:
            self.close()
