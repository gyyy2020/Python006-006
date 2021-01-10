import logging
from datetime import datetime
import pymysql

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', 
                    format='[%(levelname)s]-%(asctime)s-%(funcName)-10s-%(message)s', filename='sql.log')


def insert_data(tablename):
    '''use pymysql to insert data'''
    db = pymysql.connect('localhost', 'test', 'test', 'db1')

    try:
        with db.cursor() as cursor:
            sql = f'insert into {tablename} (person_id, person_name, person_age, person_birthday, person_gender, person_education, create_on) values (%s, %s, %s, %s, %s, %s, %s)'
            values = ((1, 'first', 11, '2020-01-01', 'male', 'Bachelor', datetime.now()), 
                (2, 'second', 22, '2020-02-01', 'female', 'Master', datetime.now()),
                (3, 'third', 33, '2020-11-01', 'male', 'highschool', datetime.now()))
            cursor.executemany(sql, values)
        db.commit()
    except Exception as e:
        logging.debug(f'insert error {e}')
    finally:
        db.close()
        logging.debug(cursor.rowcount)


if __name__ == "__main__":
    insert_data('personform')
