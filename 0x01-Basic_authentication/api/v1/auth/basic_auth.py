#!/usr/bin/env python3
"""
Basic authorization schema module
"""
from base64 import b64encode, b64decode
from binascii import Error
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Implementing basic-auth style
    """
    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """
        Extract the encoded creadential from the authorization_header
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        auth = authorization_header[6:]
        return auth

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """Decode the base64 authorization header value into utf-8
        """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            auth_str = b64decode(base64_authorization_header).decode("utf-8")
            return auth_str
        except (Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract the user credentials from the
        decoded_base64_authorization_header string,
        and return (user_name, password) tuple
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        credents = decoded_base64_authorization_header.split(":")
        try:
            return (credents[0], credents[1])
        except IndexError:
            return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """Returns a User instance based on the user_email and user_pwd, or
        None if there is no user with these credentials
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})[0]
            if not user:
                return None
            if not user.is_valid_password(user_pwd):
                return None
            return user
        except IndexError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current active user
        Parameters:
        ------------
        request: flask.request object
        """
        encoded_auth = self.extract_base64_authorization_header(
            self.authorization_header(request)
        )
        auth = self.decode_base64_authorization_header(encoded_auth)
        if not auth:
            return None
        user_email, user_pwd = self.extract_user_credentials(auth)
        if not user_email or not user_pwd:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)
