#!/usr/bin/env python3

""" auth Module """

from flask import request
from typing import List, TypeVar
import re
from os import getenv

SESSION_NAME = getenv("SESSION_NAME")


class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method """
        if not path or not excluded_paths:
            return True
        clean_path = re.escape(path)
        for ex_path in excluded_paths:
            if ex_path.endswith("*"):
                new_path = ex_path[:-1]
                if re.search(f"^{new_path}", clean_path):
                    return False
            elif re.match(f"^{clean_path}/?$", ex_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ current_user """
        return None

    def session_cookie(self, request=None):
        """ This method returns a session id from cookies """
        if request is None:
            return None
        session_id = request.cookies.get(SESSION_NAME)
        return session_id
