#!/usr/bin/env python3
"""Auth module that holds the authentication service
"""
from bcrypt import hashpw, gensalt
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and return the hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user with the given email and password.
        return the User object.
        Raise valueError if the email already exists in the database.
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        user = self._db.add_user(email, _hash_password(password))
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate the login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
