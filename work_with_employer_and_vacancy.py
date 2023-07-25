class Employer:
    """Класс для работы с компаниями"""

    def __init__(self, employer_id, name, url, vacancies_url, open_vacancies, description):
        self.employer_id = employer_id
        self.name = name
        self.url = url
        self.vacancies_url = vacancies_url
        self.open_vacancies = open_vacancies
        self.description = description

    def __repr__(self):
        return f'{self.employer_id} {self.name} {self.url} {self.vacancies_url} {self.open_vacancies} {self.description} '

    def __str__(self):
        return f'{self.employer_id} {self.name} {self.url} {self.vacancies_url} {self.open_vacancies} {self.description} '

    @property
    def json_format(self):
        """Метод, возвращающий данные по компании в формате json"""
        return {
            'employer_id': self.employer_id,
            'name': self.name,
            'url': self.url,
            'vacancies_url': self.vacancies_url,
            'open_vacancies': self.open_vacancies,
            'description': self.description,

        }


class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, vacancy_id, name, employer_name, employer_id, url, salary_from, salary_to, description, area):
        self.vacancy_id = vacancy_id
        self.name = name
        self.employer_name = employer_name
        self.employer_id = employer_id
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description
        self.area = area

    def __repr__(self):
        return f'{self.vacancy_id} {self.name} {self.employer_name} {self.employer_id} {self.url} {self.salary_from} {self.salary_to} {self.description} {self.area} '

    def __str__(self):
        return f'{self.vacancy_id} {self.name} {self.employer_name} {self.employer_id} {self.url} {self.salary_from} {self.salary_to} {self.description} {self.area} '

    @property
    def middle_salary(self):
        """Метод, возвращающий среднюю зарплату"""
        if self.salary_from and self.salary_to:
            middle_salary = (self.salary_from + self.salary_to) // 2
            return middle_salary
        return self.salary_to or self.salary_from

    @property
    def json_format(self):
        """Метод, возвращающий данные по вакансии в формате json"""
        return {
            'vacancy_id': self.vacancy_id,
            'name': self.name,
            'employer_name': self.employer_name,
            'employer_id': self.employer_id,
            'url': self.url,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'middle_salary': self.middle_salary,
            'description': self.description,
            'area': self.area,
        }

