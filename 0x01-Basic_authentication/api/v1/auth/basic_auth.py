#!/usr/bin/env python3
"""
Basic authorization sechema module holds teh BasicAuth
"""
from base64 import b64decode
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Implementing basic-auth authonitication sechema
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
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
            self, base64_authorization_header: str) -> str:
        """Decode the base64 authorization header value into utf-8
        """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            auth_str = b64decode(base64_authorization_header).decode("utf-8")
            return auth_str
        except Exception:
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
