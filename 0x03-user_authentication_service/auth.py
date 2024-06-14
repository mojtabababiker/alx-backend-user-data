#!/usr/bin/env python3
"""Auth module that holds the authentication service
"""
from uuid import uuid4
from bcrypt import hashpw, gensalt
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _generate_uuid() -> str:
    """Generates a UUID"""
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and return the hashed password"""
    return hashpw(password.encode("utf-8"), gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

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
        return True if the creadentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Generates a session ID for the user with email email.
        save it to the database and return the session ID.
        return None if the email is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrive a user from the database based on the session_id
        and return the user object, returns None if there no
        user is found
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """Destroy the session of the user with id user_id
        if the user exists
        """
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for the user with email email
        and saves it in the database.
        return the token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Rest user password if the reset_token is valid"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                user.id, hashed_password=_hash_password(password), reset_token=None
            )
        except NoResultFound:
            raise ValueError
