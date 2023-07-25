from configparser import ConfigParser
import psycopg2


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def create_database(database_name: str, params: dict):
    """Создание базы данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()


def create_employers_table(cursor):
    """Создание таблицы employers"""

    cursor.execute("""
        CREATE TABLE employers (
            employer_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            url VARCHAR NOT NULL,
            vacancies_url VARCHAR NOT NULL,
            open_vacancies INTEGER,
            description TEXT
            )
        """)


def create_vacancies_table(cursor):
    """Создание таблицы vacancies"""

    cursor.execute("""
        CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            employer_name VARCHAR NOT NULL,
            employer_id SERIAL,
            url VARCHAR NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            middle_salary INTEGER,
            description TEXT,
            area VARCHAR NOT NULL
            )
        """)


def insert_employers_data(cursor, employer):
    """Заполнение таблицы employers данными"""

    cursor.execute(
        """
        INSERT INTO employers (employer_id, name, url, vacancies_url, open_vacancies, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (employer.employer_id, employer.name, employer.url,
         employer.vacancies_url, employer.open_vacancies, employer.description)
    )


def insert_vacancies_data(cursor, vacancy):
    """Заполнение таблицы vacancies данными"""

    cursor.execute(
        """
        INSERT INTO vacancies (vacancy_id, name, employer_name, employer_id, url, salary_from, salary_to, middle_salary, description, area)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (vacancy.vacancy_id, vacancy.name, vacancy.employer_name, vacancy.employer_id, vacancy.url, vacancy.salary_from,
         vacancy.salary_to, vacancy.middle_salary, vacancy.description, vacancy.area)
    )


def add_foreign_key(cursor):
    """Добавление связи между таблицами"""

    cursor.execute("""
        ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers FOREIGN KEY(employer_id) REFERENCES employers(employer_id);
        """)

