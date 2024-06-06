#!/usr/bin/env python3
"""
Session basef authonetication model
"""
from uuid import uuid4
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Session authorization class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create a session id for the current user with id
        use id, and savee it into session bool
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_session_id[session_id] = user_id
        return session_id
