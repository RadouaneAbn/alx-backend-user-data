#!/usr/bin/env python3
""" auth Module """
import bcrypt
from typing import ByteString


def _hash_password(password: str) -> ByteString:
    """ This function return a hashed password """
    return bcrypt.hashpw(password.encode(), salt=bcrypt.gensalt())
