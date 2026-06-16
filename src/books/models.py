from sqlalchemy import Column, Integer, String, Date
from src.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    published_date = Column(Date)
    language = Column(String, nullable=False)
    
    
    