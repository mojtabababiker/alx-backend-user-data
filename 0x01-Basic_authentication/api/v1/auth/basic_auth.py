#!/usr/bin/env python3
"""
Basic authorization sechema module holds teh BasicAuth
"""
from base64 import b64encode, b64decode
from binascii import Error
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Implementing basic-auth authonitication sechema
    """
