import logging
from time import perf_counter, sleep
import pymysql
from hw4_conn_pool import conn

logging.basicConfig(level=logging.DEBUG, 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    format='[%(levelname)s]-%(asctime)s-%(funcName)-10s-%(message)s', 
                    filename='sql.log')


def create_table(tablename, conn):
    '''use pymysql to create table'''

    try:
        with conn.cursor() as cursor:
            sql = f'create table `{tablename}`(\
                `id` int(10) NOT NULL AUTO_INCREMENT, \
                `name` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, \
                PRIMARY KEY (`id`) USING BTREE\
                )ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci;'
                
            cursor.execute(sql)
    except Exception as e:
        logging.debug(f'create table error {e}')
    finally:
        cursor.close()


def drop_table(tablename, conn):
    '''use pymysql to drop table'''

    try:
        with conn.cursor() as cursor:
            sql = f'drop table {tablename}'
            cursor.execute(sql)
    except Exception as e:
        logging.debug(f'drop table error {e}')
    finally:
        cursor.close()


def insert_data(tablename, conn, in_vals):
    '''use pymysql to insert data'''

    try:
        with conn.cursor() as cursor:
            sql = f'insert into {tablename} (id, name) values(%s, %s)'
            cursor.executemany(sql, in_vals)
        conn.commit()
    except Exception as e:
        logging.debug(f'insert error {e}')
    finally:
        cursor.close()
        logging.debug(cursor.rowcount)


def delete_data(tablename, conn):
    '''use pymysql to delete data'''

    try:
        with conn.cursor() as cursor:
            sql = f'delete from {tablename};'
            cursor.execute(sql)
        conn.commit()
    except Exception as e:
        logging.debug(f'delete error {e}')
    finally:
        cursor.close()
        logging.debug(cursor.rowcount)


def query_data(conn, mode='INNER'):
    '''use pymysql to query data'''

    try:
        with conn.cursor() as cursor:
            sql = f'SELECT table1.id, table1.name, table2.id, table2.name \
                FROM table1 \
                {mode} JOIN table2 \
                ON table1.id = table2.id;'
            cursor.execute(sql)
            res = cursor.fetchall()
            print(f'{mode} JOIN result: {res}')
        conn.commit()
    except Exception as e:
        logging.debug(f'query error {e}')
    finally:
        logging.debug(cursor.rowcount)


def add_index(tablename, conn):
    '''use pymysql to add index'''

    try:
        with conn.cursor() as cursor:

            sql = f'CREATE INDEX id ON {tablename} (id);'
            cursor.execute(sql)
            conn.commit()

            sql = f'CREATE INDEX name ON {tablename} (name);'
            cursor.execute(sql)
            conn.commit()

            sql = f'SHOW INDEX FROM {tablename};'
            cursor.execute(sql)
            res = cursor.fetchall()[1:]
            for r in res:
                logging.info(f'result: {r}')
        conn.commit()
    except Exception as e:
        logging.debug(f'add index error {e}')
    finally:
        logging.debug(cursor.rowcount)


def drop_index(tablename, conn, idx_name):
    '''use pymysql to drop index'''

    try:
        with conn.cursor() as cursor:
            logging.info(f'indexs: {idx_name}')

            for idx in idx_name:
                logging.info(f'current index: {idx}')
                sql = f'ALTER TABLE {tablename} DROP INDEX {idx};'
                cursor.execute(sql)
                conn.commit()

            sql = f'SHOW INDEX FROM {tablename};'
            cursor.execute(sql)
            res = cursor.fetchall()
            for r in res:
                logging.info(f'result: {r}')
            if len(res) == 1:
                logging.info('drop index success')
            else:
                logging.info('drop index fail')

        conn.commit()
    except Exception as e:
        logging.debug(f'drop index error {e}')
    finally:
        logging.debug(cursor.rowcount)


def test_hw4(loop):
    '''no index'''
    indexs = ('id', 'name')
    for t in tables:
        drop_index(t, conn, indexs)

    t0 = perf_counter()
    for _ in range(loop):
        query_data(conn, 'INNER')
        query_data(conn, 'LEFT')
        query_data(conn, 'RIGHT')
    delta_t = perf_counter() - t0
    return delta_t


def test_hw5(loop):
    '''have index'''

    indexs = ('id', 'name')
    for t in tables:
        add_index(t, conn)

    t0 = perf_counter()
    for _ in range(loop):
        query_data(conn, 'INNER')
        query_data(conn, 'LEFT')
        query_data(conn, 'RIGHT')
    delta_t = perf_counter() - t0
    return delta_t

if __name__ == "__main__":
    tables = ('table1', 'table2')
    # create_table(tables[0], conn)
    # create_table(tables[1], conn)

    # from t in tables:
    #     drop_table(t, conn)

    # values1 = ((1, 'table1_table2'), 
    #     (2, 'table1'))
    # values2 = ((1, 'table1_table2'), 
    #     (3, 'table2'))
    # insert_data(tables[0], conn, values1)
    # insert_data(tables[1], conn, values2)

    # delete_data(tables[0], conn)
    # delete_data(tables[1], conn)

    # indexs = ('id', 'name')
    # for t in tables:
    #     add_index(t, conn)
    #     drop_index(t, conn, indexs)

    # t0 = perf_counter()
    # query_data(conn, 'INNER')
    # query_data(conn, 'LEFT')
    # query_data(conn, 'RIGHT')
    # print(perf_counter() - t0)

    t1 = test_hw4(1)
    t2 = test_hw5(1)
    print(t1, t2, t1 > t2, sep='\t')

    conn.close()