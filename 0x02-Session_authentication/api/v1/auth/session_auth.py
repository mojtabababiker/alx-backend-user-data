#!/usr/bin/env python3
"""
Session basef authonetication model
"""
from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User


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
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrive the user id from session based on the
        session id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        Return a User object based on the cookie value
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        # case: no data on the database or no user with user_id
        try:
            user = User.get(user_id)
        except Exception:
            return None
        return user
