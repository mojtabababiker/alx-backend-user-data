#!/usr/bin/env python3
"""
User database model module
"""
from typing import Union
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):  # type: ignore
    """
    User Database model class
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)

    def __init__(self, email: str, hashed_password: str,
                 session_id: Union[str, None] = None,
                 reset_token: Union[str, None] = None):
        """
        construct User instance
        """
        self.email = email  # type: ignore
        self.hashed_password = hashed_password  # type: ignore
        self.session_id = session_id  # type: ignore
        self.reset_token = reset_token  # type: ignore
