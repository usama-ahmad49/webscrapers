from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
#
# connection = psycopg2.connect(
#     host='localhost',
#     database='realtordb',
#     user='postgres',
#     password='123456789',
#     port='8080'
# )
# cur = connection.cursor()

db_string = "postgresql://postgres:123456789@localhost:8080/realtordb"


def upload_data(TABLE,valueList):
    db = create_engine(db_string)
    # meta = MetaData(db)
    Table = TABLE
    with db.connect() as conn:
        # Table.create()
        try:
            insert_statement = Table.insert().values(dict(valueList))
            conn.execute(insert_statement)
        except:
            update_statement = TABLE.update().where(Table.c.id == valueList['id']).values(dict(valueList))
            conn.execute(update_statement)
# 'ON CONFLICT ( "PropertyUrl" ) DO UPDATE SET "PropertyUrl" = excluded."PropertyUrl"')
# dict({key:val for key, val in valueList.items() if key != 'id'})








# import psycopg2
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# connection = psycopg2.connect(
#             host='localhost',
#             database='realtordb',
#             user='postgres',
#             password='123456789',
#             port='8080'
#         )
# cur = connection.cursor()
#
# # class postgressUploadClient:
# def upload_data(tableName, columnsList, valueList, IDCol, IDVALUE):
#     # textCreate =f'{IDCol} character varying COLLATE pg_catalog."default" NOT NULL,'
#     # for col in columnsList[1:]:
#     #     textCreate = textCreate+f' {col} character varying COLLATE pg_catalog."default",'
#     # textCreate += f'CONSTRAINT "{tableName}_pkey" PRIMARY KEY ("{IDCol}")'
#     #
#     # '''create table if doesnt exit'''
#     #
#     # createquery = f'CREATE TABLE IF NOT EXISTS public.{tableName}({textCreate})'
#     # cur.execute(createquery)
#     # connection.commit()
#
#
#
#     text = columnsList[0]
#     value = '"'+str(IDVALUE)+'"'
#     for col in list(valueList.keys())[1:]:
#         text = text+","+col
#     for val in list(valueList.values())[1:]:
#         value = value + ','+ '"'+str(val)+'"'
#     cur.execute(f'INSERT INTO public.{tableName}({text})' + f"VALUES ({value})" + f'ON CONFLICT ( {IDCol} ) DO UPDATE SET {IDCol} = excluded.{IDCol}')
#     try:
#         connection.commit()
#         logger.info('data sent to database')
#     except:
#         logger.info('Error! data not sent to database')
