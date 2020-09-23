from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, session

from scraping import settings

Base = declarative_base()
# If we have 2 tables with same name in different databases then we get error that tables with same name
# already exists.
# Ref: https://stackoverflow.com/questions/15336778/using-same-name-of-tables-with-different-binds-in-flask
# So, we are creating another Base class here to be used.
BaseSecond = declarative_base()
# BBI Database
engine_bbi = create_engine(settings.DATABASE_URI.format(**settings.DATABASE_BBI),
                           encoding='utf-8', pool_size=20, pool_recycle=60)
db_session_bbi = scoped_session(session.sessionmaker(bind=engine_bbi, expire_on_commit=False))
META1 = MetaData(engine_bbi)
