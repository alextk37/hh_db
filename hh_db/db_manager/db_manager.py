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
        '''
          Создает и возвращает новый экземпляр класса.
        '''
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __del__(self):
        '''
        Удаляет экземпляр класса и устанавливает
         значение переменной __instance в None.
        '''
        DBManager.__instance = None

    def __init__(self, dbname, user, password, port, host='localhost'):
        '''
            Инициализирует экземпляр класса DBManager.

            Параметры:
            dbname (str): имя базы данных.
            user (str): имя пользователя для подключения к базе данных.
            password (str): пароль пользователя для подключения к базе данных.
            port (int): номер порта для подключения к базе данных.
            host (str, optional): адрес хоста базы данных.
                По умолчанию 'localhost'.
        '''
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        '''
        Устанавливает соединение с базой данных.
        '''
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
        '''
        Закрывает соединение с базой данных.
        '''
        try:
            self.conn.close()
        except AttributeError:
            print('Ошибка подключения к БД')

    def req_resp(self, prompt):
        '''
        Выполняет SQL-запрос к базе данных и возвращает результат.
        '''
        try:
            self.connect()
            self.cursor.execute(prompt)
            return self.cursor.fetchall()
        except AttributeError:
            print('Ошибка подключения к БД')
        finally:
            self.close()

    def req_not_resp(self, prompt):
        '''
        Выполняет SQL-запрос к базе данных без возвращения результата.
        '''
        try:
            self.connect()
            self.cursor.execute(prompt)
        except AttributeError:
            print('Ошибка подключения к БД')
        finally:
            self.close()
