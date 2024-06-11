#!/usr/bin/env python3
"""
DB module that holds the database engine abstract class
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class, is databse engine abstract class that manage all the
    databse operations
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object privite property
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()  # type: ignore
        return self.__session  # type: ignore

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create a new user with the email and password,
        return the new user object
        """
        user = User(email=email, hashed_password=hashed_password)  # type: ignore

        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs: dict) -> User:
        """
        Find and return the first user that match the parameters
        on the kwargs
        NoResultFound will be raised when the are no result with those
        parameters
        InvalidRequestError will be raised when query (kwargs) contains
        wrong arguments
        """
        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound()
        return user
