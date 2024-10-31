from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

user_subject_relation = Table(
    'user_subject_relation',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_date = Column(Date)

    address_id = Column(Integer, ForeignKey('addresses.id'))

    subjects = relationship (
        "SubjectModel",
        secondary=user_subject_relation,
        back_populates="users"
    )



class SubjectModel(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationship
    users = relationship(
        "UserModel",
        secondary=user_subject_relation,
        back_populates="subjects"
    )



class AddressModel(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String, index=True) # to create an index on a field
    house_num = Column(Integer)

    users = relationship("UserModel", back_populates="address")

    __table_args__ = (
        Index('ix_addresses_city_street', 'city', 'street'),
    )
