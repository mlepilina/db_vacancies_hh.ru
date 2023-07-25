from abc import ABC, abstractmethod
import requests
from work_with_employer_and_vacancy import Employer, Vacancy


class PlatformsAPI(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями"""

    @abstractmethod
    def get_employers(self, count, page) -> list[Employer]:
        """
        Получение компаний.

        :count - это кол-во элементов на странице
        :page - это номер страницы
        """

    @abstractmethod
    def get_employers_by_id(self, employer_id) -> list[Employer]:
        """
        Получение информации о компании по её id.
        """

    @abstractmethod
    def get_vacancies(self, employer_id) -> list[Vacancy]:
        """
        Получение вакансий по id компании.
        """


class HeadHunterAPI(PlatformsAPI):
    """
    Получение компаний и вакансий с сайта hh.ru
    """

    def __init__(self):
        self.api_url = 'https://api.hh.ru'

    def get_employers(self, count=100, page=0):
        url = self.api_url + '/employers'
        params = {"per_page": count, "page": page, "only_with_vacancies": True}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return []

        data = response.json()
        employers = []
        for employer in data['items']:

            employers.append(
                Employer(
                    employer_id=employer['id'],
                    name=employer['name'],
                    url=employer['alternate_url'],
                    vacancies_url=employer['vacancies_url'],
                    open_vacancies=employer['open_vacancies'],
                    description=None,
                )
            )

        return employers

    def get_employers_by_id(self, employer_id):
        url = self.api_url + f'/employers/{employer_id}'
        response = requests.get(url)
        if response.status_code != 200:
            return []

        data = response.json()

        employer = Employer(
            employer_id=data['id'],
            name=data['name'],
            url=data['alternate_url'],
            vacancies_url=data['vacancies_url'],
            open_vacancies=data['open_vacancies'],
            description=data['description'])

        return employer

    def get_vacancies(self, employer_id):
        url = self.api_url + f'/vacancies?employer_id={employer_id}'
        response = requests.get(url)
        if response.status_code != 200:
            return []

        data = response.json()
        vacancies = []
        for vacancy in data['items']:

            if vacancy['salary']:
                salary_from = vacancy['salary'].get('from') or 0
                salary_to = vacancy['salary'].get('to') or 0
            else:
                salary_from = 0
                salary_to = 0

            vacancies.append(
                Vacancy(
                    vacancy_id=vacancy['id'],
                    name=vacancy['name'],
                    employer_name=vacancy['employer']['name'],
                    employer_id=vacancy['employer']['id'],
                    url=vacancy['alternate_url'],
                    salary_from=salary_from,
                    salary_to=salary_to,
                    description=vacancy['snippet']['responsibility'],
                    area=vacancy['area']['name'],
                )
            )

        return vacancies

