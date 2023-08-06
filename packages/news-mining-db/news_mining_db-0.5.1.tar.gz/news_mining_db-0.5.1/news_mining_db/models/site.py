from sqlalchemy.orm import relation

from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String


class Site(Base):
    __tablename__ = 'site'

    id = Column(Integer, primary_key=True)

    name = Column(String(32))

    rss_link = Column(String(64))
    link = Column(String(64))

    prev_hash = Column(String(64))

    news = relation('News', back_populates='site')
