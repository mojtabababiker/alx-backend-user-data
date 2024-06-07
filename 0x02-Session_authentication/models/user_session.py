#!/usr/bin/env python3
"""
Database model for user session
"""
from models.base import Base


class UserSession(Base):
    """
    User session database model
    """
    def __init__(self, *args, **kwargs):
        """
        initiate user_id and session_id, and calling the super()
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
