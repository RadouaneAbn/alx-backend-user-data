#!/usr/bin/env python3
""" basic_auth Module """
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar
import base64
import binascii


class BasicAuth(Auth):
    """ BasicAuth class """
    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """ This method extracts the Base64 part
            of the Authorization header
        """
        if authorization_header is None\
            or type(authorization_header) != str\
                or not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """ This method return a decoded value of a Base64 string """
        if base64_authorization_header is None\
                or type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header
            ).decode("utf-8")
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """ This method return the email and password in decoded string """
        if decoded_base64_authorization_header is None\
            or type(decoded_base64_authorization_header) != str\
                or ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):   # type: ignore
        """ This method return a user instance
            if found with correct password
        """
        if user_email is None or user_pwd is None\
                or type(user_email) != str or type(user_pwd) != str:
            return None
        try:
            user = User.search({"email": user_email})
        except KeyError:
            return None
        if not user or not user[0].is_valid_password(user_pwd):
            return None
        return user[0]
