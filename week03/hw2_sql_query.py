import logging
import pymysql

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', 
                    format='[%(levelname)s]-%(asctime)s-%(funcName)-10s-%(message)s', filename='sql.log')


def query_data(tablename):
    '''use pymysql to query data'''
    db = pymysql.connect('localhost', 'test', 'test', 'db1')

    try:
        with db.cursor() as cursor:
            sql = f'select * from {tablename}'
            cursor.execute(sql)
            persons = cursor.fetchall()
            for p in persons:
                logging.debug(p)
        db.commit()
    except Exception as e:
        logging.debug(f'query error {e}')
    finally:
        db.close()
        logging.debug(cursor.rowcount)


if __name__ == "__main__":
    query_data('personform')