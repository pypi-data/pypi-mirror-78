from sqlalchemy.orm import relation

from news_mining_db.models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Text


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)

    site_id = Column(Integer, ForeignKey('site.id', ondelete='CASCADE'))
    site = relation('Site', back_populates="news")

    title = Column(String(256))

    text = Column(Text())
