#!/usr/bin/env python3
"""Auth module that holds the authentication service
"""
from bcrypt import hashpw, gensalt

def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and return the hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt())
