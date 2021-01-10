import logging
from datetime import datetime
from time import perf_counter
import pymysql
from hw4_conn_pool import conn

logging.basicConfig(level=logging.DEBUG, 
                    datefmt='%Y-%m-%d %H:%M:%S', 
                    format='[%(levelname)s]-%(asctime)s-%(funcName)-10s-%(message)s', 
                    filename='sql_hw6.log')


def create_table(sqlcmd, conn):
    '''use pymysql to create table'''

    try:
        with conn.cursor() as cursor:                
            cursor.execute(sqlcmd)
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


def insert_data(tablename, conn, in_col, in_vals):
    '''use pymysql to insert data'''

    try:
        with conn.cursor() as cursor:
            sql = f'insert into {tablename} ({in_col[0]}, {in_col[1]}) values(%s, %s)'
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


def update_data(tablename, conn, count, user_id, affairs=True):
    '''use pymysql to update data'''

    try:
        with conn.cursor() as cursor:
            sql = f'update {tablename} set user_assets=user_assets+{count} where user_id={user_id}'
            cursor.execute(sql)
        if affairs:
            pass
        else:
            conn.commit()
    except Exception as e:
        logging.debug(f'update error {e}')
    finally:
        cursor.close()
        logging.debug(cursor.rowcount)


def query_data(conn, table, cmd=''):
    '''use pymysql to query data'''

    res = object()
    try:
        with conn.cursor() as cursor:
            sql = f'SELECT * from {table};' if not cmd else cmd
            cursor.execute(sql)
            res = cursor.fetchall()
    except Exception as e:
        logging.debug(f'query error {e}')
    finally:
        logging.debug(cursor.rowcount)
        return res


def insert_transaction(conn, in_col, in_vals):
    '''use pymysql to insert data'''

    try:
        with conn.cursor() as cursor:
            sql = f'insert into table_transactions (\
                {in_col[0]}, {in_col[1]}, {in_col[2]}, {in_col[3]}, {in_col[4]}) \
                values(%s, %s, %s, %s, %s)'
            cursor.execute(sql, in_vals)
    except Exception as e:
        logging.debug(f'insert error {e}')
    finally:
        cursor.close()
        logging.debug(cursor.rowcount)


def test6_1(tables):
    '''create 3 tables'''
    print(tables)
    sqls = (f'create table `{tables[0]}`(\
                `user_id` int(10) NOT NULL AUTO_INCREMENT, \
                `user_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL, \
                PRIMARY KEY (`user_id`) USING BTREE\
                )ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;',
                f'create table `{tables[1]}`(\
                `user_id` int(10) NOT NULL AUTO_INCREMENT, \
                `user_assets` int(20), \
                PRIMARY KEY (`user_id`) USING BTREE\
                )ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci;',
                f'create table `{tables[2]}`(\
                `tran_id` int(10) NOT NULL AUTO_INCREMENT, \
                `tran_time` datetime NOT NULL, \
                `send_id` int(10) NOT NULL, \
                `recv_id` int(10) NOT NULL, \
                `tran_count` int(10) NOT NULL, \
                PRIMARY KEY (`tran_id`) USING BTREE\
                )ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci;'
            )
    for sql in sqls:
        create_table(sql, conn)


def test6_2(tables):
    '''add test data'''
    column1 = ('user_id', 'user_name')
    column2 = ('user_id', 'user_assets')
    values1 = ((1, 'zhangsan'), (2, 'lisi'))
    values2 = ((1, 10), (2, 666))

    insert_data(tables[0], conn, column1, values1)
    insert_data(tables[1], conn, column2, values2)


def test6_3(tables, conn, count):
    '''affairs'''
    # 得出user_id
    cmd1 = 'select user_id from table_user where user_name="zhangsan"'
    cmd2 = 'select user_id from table_user where user_name="lisi"'
    try:
        id1 = query_data(conn, tables[0], cmd1)[0][0]
        id2 = query_data(conn, tables[0], cmd2)[0][0]
    except Exception as e:
        logging.debug(e)

    # 得出余额
    cmd1 = f'select user_assets from table_assets where user_id={id1}'
    cmd2 = f'select user_assets from table_assets where user_id={id2}'
    try:
        cash1 = query_data(conn, tables[0], cmd1)[0][0]
        cash2 = query_data(conn, tables[0], cmd2)[0][0]
    except Exception as e:
        logging.debug(e)

    # 更新资产表，添加转账表记录
    try:
        count = float(count)
        if count <= 0:
            logging.info('must be a positive number. Abort')
            return False
        if (cash1 - count)> 0:
            logging.info('check ok')
        else:
            logging.info('There is not enough money in your account. Abort')
            return False
    except Exception as e:
        logging.warn(e)

    update_data(tables[1], conn, -count, id1)
    update_data(tables[1], conn, count, id2)
    col = ('tran_id', 'tran_time', 'send_id', 'recv_id', 'tran_count')
    val = (1, datetime.now(), id1, id2, count)
    insert_transaction(conn, col, val)
    conn.commit()


def test6_4(tables, conn):
    # 事务执行前后各查询一次
    names = ('zhangsan', 'lisi')
    cmd1 = f'select user_assets from table_user, table_assets where (table_user.user_id=table_assets.user_id and user_name="{names[0]}")'
    cmd2 = f'select user_assets from table_user, table_assets where (table_user.user_id=table_assets.user_id and user_name="{names[1]}")'

    try:
        assets1 = query_data(conn, tables[0], cmd1)[0][0]
        assets2 = query_data(conn, tables[0], cmd2)[0][0]
        transaction = query_data(conn, tables[2])
        logging.info(f'\n {names[0]} assets: {assets1} \n {names[1]} assets: {assets2}\n transaction: {transaction}')
    except Exception as e:
        logging.warn(f'query data fail: {e}')


if __name__ == "__main__":
    tables = ('table_user', 'table_assets', 'table_transactions')
    # test6_1(tables)  # 新建3张表
    # test6_2(tables)  # 添加测试数据
    logging.info('before transfer')
    test6_4(tables, conn)  # 查询各自资产变化情况
    test6_3(tables, conn, 196.78)  # 转账事务
    logging.info('after transfer')
    test6_4(tables, conn)  # 查询各自资产变化情况

    conn.close()
