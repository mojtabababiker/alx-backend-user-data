#!/usr/bin/env python3
"""DB module that holds the database engine abstract class
"""
from typing import Any, Dict
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class, is databse engine abstract class that manage all the
    databse operations
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
        """Memoized session object private property
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user with the email and password,
        return the new user object
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password

        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        """Find and return the first user that match the parameters
        on the kwargs
        NoResultFound will be raised when the are no result with those
        parameters
        InvalidRequestError will be raised when query (kwargs) contains
        wrong arguments
        """
        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound
        return user
