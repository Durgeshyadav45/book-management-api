from sqlalchemy import Column, Integer, String
from src.db.database import Base



class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique= True)
    password_hash = Column(String)
    role = Column(String, default="user")

















# from sqlmodel import SQLModel, Field, Column
# import sqlalchemy.dialects.postgresql as pg
# from datetime import datetime
# import uuid


# class User(SQLModel, table=True):
#     __tablename__ = "users"
#     uid: uuid.UUID = Field(sa_column=Column( pg.UUID(as_uuid=True),primary_key=True,default=uuid.uuid4, nullable=False) )

#     username: str = Field(nullable=False)
#     email: str = Field(nullable=False,unique=True,index=True)
#     first_name: str | None = Field(default=None)
#     last_name: str | None = Field(default=None)
#     is_verified: bool = Field(default=False)
#     password_hash: str = Field(nullable=False)
#     created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.utcnow,nullable=False))
#     updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow,nullable=False))


#     def __repr__(self):
#         return f"<User {self.username}>"