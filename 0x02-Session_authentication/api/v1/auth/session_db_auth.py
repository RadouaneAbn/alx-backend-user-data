#!/usr/bin/env python3
""" session_db_auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """ This method creates a session """
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session_dict = {
            "user_id": user_id,
            "session_id": session_id
        }
        user_session = UserSession(**user_session_dict)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ This method returns a user_id
        """
        if session_id is None:
            return None
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if not user_session:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id
        print("User:", user_session.__dict__)
        if user_session.created_at +\
                timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ This method destroies a session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return False
        if not user_session:
            return False
        user_session[0].remove()
        return True
