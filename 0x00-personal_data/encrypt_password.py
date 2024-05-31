#!/usr/bin/env python3
"""
using bcrypt package to hash user password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    get a password string and return a hashed version
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    check if the two password are matched or not
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
