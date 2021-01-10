import logging
from datetime import datetime
import pymysql
from sqlalchemy import create_engine, Table, Column, Integer, String, VARCHAR, DateTime, Date, MetaData
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', 
                    format='[%(levelname)s]-%(asctime)s-%(funcName)-10s-%(message)s', filename='sql.log')

Base = declarative_base()


class PersonTable(Base):
    __tablename__ = 'personform'
    person_id = Column(Integer(), primary_key=True)
    person_name = Column(String(20), nullable=True)
    person_age = Column(Integer())
    person_birthday = Column(Date())
    person_gender = Column(VARCHAR(10))
    person_education = Column(String(128))
    create_on = Column(DateTime(), default=datetime.now)
    update_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


def create_table():
    dburl = 'mysql+pymysql://test:test@localhost:3306/db1?charset=utf8mb4'
    engine = create_engine(dburl, echo=False, encoding='utf-8')
    Base.metadata.create_all(engine)
