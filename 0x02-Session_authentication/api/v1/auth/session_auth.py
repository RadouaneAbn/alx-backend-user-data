#!/usr/bin/env python3
""" session_auth Module
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from flask import jsonify


class SessionAuth(Auth):
    """ SessionAth class for session authentication
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ This method creates a session and returns the session id
        """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ This method returns the user id based on the session id
        """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """ This method get the current user instance """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user
