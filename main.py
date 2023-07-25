from creating_database import config, create_database, create_employers_table, create_vacancies_table, \
    insert_employers_data, insert_vacancies_data, add_foreign_key
from get_employers import HeadHunterAPI
import psycopg2


def main():
    # Получение данных о работодателях с сайта hh.ru
    employers_parsing = HeadHunterAPI().get_employers(count=100, page=0)

    # id десяти работодателей
    employers_ids = [3529, 80, 2324020, 41862, 3776, 1740, 84585, 3127, 2492, 1057]

    # создание базы данных
    db_name = 'hh_vacancies'
    params = config()

    create_database(database_name=db_name, params=params)

    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})

    # создание таблиц и заполнение их данными с сайта hh.ru
    conn = None

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_employers_table(cur)
                print(f"Таблица employers успешно создана")

                create_vacancies_table(cur)
                print("Таблица vacancies успешно создана")

                add_foreign_key(cur)
                conn.commit()
                for emp_id in employers_ids:
                    employer = HeadHunterAPI().get_employers_by_id(emp_id)
                    insert_employers_data(cur, employer)
                print("Данные в employers успешно добавлены")

                for emp_id in employers_ids:
                    vacancies = HeadHunterAPI().get_vacancies(emp_id)
                    for vacancy in vacancies:
                        insert_vacancies_data(cur, vacancy)
                print("Данные в vacancies успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    main()

