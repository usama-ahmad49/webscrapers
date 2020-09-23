from datetime import datetime, date

from sqlalchemy import Column, Date, Integer, Float, String, DateTime, Boolean, ForeignKey, UniqueConstraint

from scraping.mixin import QueryMixinBBI


class Twitter(QueryMixinBBI):
    __tablename__ = 'twitter'

    id = Column(Integer, primary_key=True)
    tweetId = Column(String(250), unique=True)
    tweetCreatedDate = Column(DateTime, default=datetime.now)
    followersCount = Column(String(50))
    followersCountOnCreatedDate = Column(String(50))
    userName = Column(String(50))
    userId = Column(String(50))
    text = Column(String(50))
    retweetCount = Column(String(50))
    favoriteCount = Column(String(50))
    replies = Column(String(50))
    engagement = Column(String(50))
    engagementRate = Column(String(50))
    media = Column(String(5000))

    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
