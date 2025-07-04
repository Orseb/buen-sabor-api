from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class BaseModel(base):

    __abstract__ = True

    id_key = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
