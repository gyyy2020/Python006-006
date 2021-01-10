from hw2_orm_create import PersonTable, create_table
from hw2_sql_insert import insert_data
from hw2_sql_query import query_data


table_name = PersonTable.__tablename__
print(table_name)

# create_table()
# insert_data(table_name)
query_data(table_name)