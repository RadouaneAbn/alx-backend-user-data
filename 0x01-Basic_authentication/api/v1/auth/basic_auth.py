#!/usr/bin/env python3
""" basic_auth Module """
from api.v1.auth.auth import Auth


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
