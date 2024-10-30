from sqlalchemy import Column, Integer, String, Date

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
