from typing import Tuple
import os
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session as SessionType


def create_db(db_name: str, **kwargs) -> Tuple[Engine, SessionType]:
    """
    Creates SQLite database connection and returns the engine and Session class.
    
    :param name: Name of the database (will create a file with a .sqlite3 extension).
    :param kwargs: Additional keyword arguments for sessionmaker, such as autocommit, autoflush.
    :raises TypeError: If an invalid keyword or value is passed to sessionmaker.
    """
    
    engine = create_engine(f"sqlite:///{db_name}.sqlite3", echo=True)
    
    try:
        
        Session = sessionmaker(bind=engine, **kwargs)
    except TypeError as ex:
        raise TypeError(f"Wrong keyword or value in the arguments: {ex}")
    
    return (engine, Session)


class classproperty:
    def __init__(self, method):
        self.method = method
    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        return self.method(cls)
    
    
class Base(DeclarativeBase):
    """
    Base class for every SQLAlchemy model that
    automatically generates table name (SQLAlchemy model name + "s")

    e.g. model "User" -> __tablename__="users"
    """

    @classproperty
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
   
    
engine = create_engine(f"sqlite:///backend/db.sqlite3", echo=True)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)