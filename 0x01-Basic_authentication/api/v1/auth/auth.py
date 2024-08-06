#!/usr/bin/env python3

""" auth Module """

from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method """
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization_header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ current_user """
        return None
