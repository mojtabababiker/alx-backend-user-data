#!/usr/bin/env python3
"""
Authorization handling module
"""
import os
import re
from typing import TypeVar, List
from flask import request


class Auth:
    """
    the authorization main class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the path is require an authonitcation for the current
        instance(user) or not according to the excluded_paths list

        Return:
        ------
        bool: True if it requires Flase otherwise
        """
        if not path or not excluded_paths:
            return True
        for p in excluded_paths:
            if re.search(path, p):
                return False
            if p.endswith("*") and re.search(p[:-1], path):
                return False
        return True

    def authorization_header(self, request: request = None) -> str:
        """
        Get the authorization header and decode its value

        Parameters:
        -----------
        request: flask.request object

        Return:
        ----------
        auth_val: str, the value of the authorization header
        """
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        Get the current active user
        Parameters:
        ------------
        request: flask.request object
        """
        return None

    def session_cookie(self, request=None):
        """
        get the coolie value from thw request and returns it
        """
        if request is None:
            return None

        session_name = os.environ.get("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
