#!/usr/bin/env python3
""" session_exp_auth Module """
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


SESSION_DURATION = getenv("SESSION_DURATION")


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class that inherits from SessionAuth """
    def __init__(self) -> None:
        """ init method that initiat an instance of the class """
        try:
            self.session_duration = int(SESSION_DURATION)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None) -> str:
        """ This method create a session """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {}
        session_dict["user_id"] = user_id
        session_dict["created_at"] = datetime.now()
        self.user_id_by_session_id[session_id] = {
            "session dictionary": session_dict
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ This method return an id using a session id """
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id, None)
        if session_id is None:
            return None
        session_dict = session_dict["session dictionary"]
        if self.session_duration <= 0:
            return session_dict["user_id"]
        if not session_dict.get("created_at", None):
            return None
        if session_dict["created_at"] +\
                timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return session_dict["user_id"]
