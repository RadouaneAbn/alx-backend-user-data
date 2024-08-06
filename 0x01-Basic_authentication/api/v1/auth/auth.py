#!/usr/bin/env python3

""" auth Module """

from flask import request, Request
from typing import List, TypeVar
import re


class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method """
        if not path or not excluded_paths:
            return True
        clean_path = re.escape(path)
        for ex_path in excluded_paths:
            if re.match(f"^{clean_path}/?$", ex_path):
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
