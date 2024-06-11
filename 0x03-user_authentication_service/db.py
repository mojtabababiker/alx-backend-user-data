
#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
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
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()  # type: ignore
        return self.__session  # type: ignore

    def add_user(self, email: str, hashed_password: str,
                 **kwargs: dict) -> User:
        """
        Create a new user with the email and password,
        return the new user object
        """
        user = User()
        user.email = email
        user.hashed_password = hashed_password

        self.__session.add(user)  # type: ignore
        self.__session.commit()  # type: ignore

        return user
