#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base
from typing import Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ create and save a new user """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ This method finds a user usong keyword arguments """
        if not all(hasattr(User, key) for key in kwargs.keys()):
            raise InvalidRequestError()
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound()
        return user

    def update_user(self, user_id: str, **kwargs: Dict) -> None:
        """ This method updates a user """
        user = self.find_user_by(id=user_id)
        if not all(hasattr(User, key) for key in kwargs.keys()):
            raise ValueError()
        for k, v in kwargs.items():
            setattr(user, k, v)
        return None
