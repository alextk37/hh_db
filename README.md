# Проект сбора данных о вакансиях

## Описание

Данный проект предназначен для сбора данных о вакансиях и сохранения их в базу данных PostgreSQL.

## Технологии

    База данных: PostgreSQL
    Библиотека для работы с PostgreSQL в Python: psycopg2
    Управление зависимостями: poetry


## Установка

    Установите PostgreSQL, если он не установлен!
    Установите poetry, если он не установлен.
    Установите необходимые зависимости, запустив poetry install в корневом каталоге проекта.


## Настройка

    Укажите необходимые параметры подключения к базе данных PostgreSQL в файле config.py.
    Укажите ключевые слова для поиска вакансий в файле company_config.py.


## Запуск

Запустите main.py для запуска процесса сбора данных о вакансиях и их сохранения в базу данных.
