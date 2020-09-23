from datetime import datetime, date

from sqlalchemy import Column, Date, Integer, Float, String, DateTime, Boolean, ForeignKey, UniqueConstraint

from scraping.mixin import QueryMixinBBI


class Golmark(QueryMixinBBI):
    __tablename__ = 'glomark'

    id = Column(Integer, primary_key=True)
    globalId = Column(Integer)
    url = Column(String(350))
    name = Column(String(200))
    price = Column(String(100))
    createdDate = Column(String(100))
    imageUrl = Column(String(350))
    category = Column(String(100))

    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GlobalId(QueryMixinBBI):
    __tablename__ = 'global_id'

    id = Column(Integer, primary_key=True)
    taken = Column(String(10))
