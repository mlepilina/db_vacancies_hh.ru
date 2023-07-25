import psycopg2


class DBManager:

    def __init__(self, host, db_name, user, password, port):
        self.conn = psycopg2.connect(host=host, database=db_name, user=user, password=password, port=port)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        conn = self.conn
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""SELECT name, open_vacancies FROM employers""")
        data = cur.fetchall()
        conn.close()
        return data

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        conn = self.conn
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""SELECT name, employer_name, salary_from, salary_to, url FROM vacancies""")
        data = cur.fetchall()
        conn.close()
        return data

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        conn = self.conn
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
        SELECT AVG(middle_salary) as avg_salary FROM vacancies
        WHERE middle_salary <> 0
        """)
        data = cur.fetchone()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        conn = self.conn
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
        SELECT name, salary_from, salary_to FROM vacancies
        WHERE salary_from > (SELECT AVG(middle_salary) FROM vacancies WHERE middle_salary <> 0) OR salary_to > (SELECT AVG(middle_salary) FROM vacancies WHERE middle_salary <> 0)
        """)
        data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, keywords: list):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = self.conn
        conn.autocommit = True
        cur = conn.cursor()
        data = []

        for keyword in keywords:
            cur.execute(f"""
                    SELECT name FROM vacancies
                    WHERE name LIKE '%{keyword}%'
                    """)
            data.append(cur.fetchall())

        conn.close()
        return data


# тест
companies_and_vacancies_count = DBManager('localhost', 'hh_vacancies', 'postgres', 1234, 5432).get_companies_and_vacancies_count()
print(companies_and_vacancies_count)

all_vacancies = DBManager('localhost', 'hh_vacancies', 'postgres', 1234, 5432).get_all_vacancies()
print(all_vacancies)

avg_salary = DBManager('localhost', 'hh_vacancies', 'postgres', 1234, 5432).get_avg_salary()
print(avg_salary)

vacancies_with_higher_salary = DBManager('localhost', 'hh_vacancies', 'postgres', 1234, 5432).get_vacancies_with_higher_salary()
print(vacancies_with_higher_salary)

vacancies_with_keyword = DBManager('localhost', 'hh_vacancies', 'postgres', 1234, 5432).get_vacancies_with_keyword(['офис', 'менеджер'])
print(vacancies_with_keyword)

