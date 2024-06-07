#!/usr/bin/env python3
"""
Time expiration session auth based module
"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Time expiration session auth based class
    """
    def __init__(self):
        """
        set the time duration for the instance
        """
        self.session_duration = int(
            os.environ.get("SESSION_DURATION", 0)
        )

    def create_session(self, user_id=None):
        """
        overload super create_session to add the time duration
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        overload: retrive the user id from session based on the
        session id, and implement the expire logic
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        session = self.user_id_by_session_id.get(session_id, None)
        if session is None:
            return None
        if self.session_duration <= 0:
            return session.get("user_id", None)
        created_at = session.get("created_at", None)
        if created_at is None:
            return None
        seconds = timedelta(seconds=self.session_duration)
        if created_at + seconds < datetime.now():
            return None
        return session.get("user_id", None)
