#!/usr/bin/env python3
""" auth Module """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ This function return a hashed password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
