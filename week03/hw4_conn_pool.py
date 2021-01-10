import pymysql
from dbutils.pooled_db import PooledDB

db_config = {
    'host':'localhost',
    'port':3306,
    'user':'test',
    'passwd':'test',
    'db':'db1',
    'charset':'utf8mb4',
    'maxconnections':0,
    'mincached':4,
    'maxcached':0,
    'maxusage':5,
    'blocking':True
}

spool = PooledDB(pymysql, **db_config)
conn = spool.connection()
