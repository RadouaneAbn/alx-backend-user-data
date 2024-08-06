#!/usr/bin/env python3
""" basic_auth Module """
from api.v1.auth.auth import Auth
from typing import Tuple
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
