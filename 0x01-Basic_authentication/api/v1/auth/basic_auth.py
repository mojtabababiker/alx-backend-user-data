#!/usr/bin/env python3
"""
Basic authorization sechema module holds teh BasicAuth
"""
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
