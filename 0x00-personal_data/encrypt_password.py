#!/usr/bin/env python3
"""
encrypt_password Module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ This function hashes a password and returns the hashed password """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                    bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ This function checkes wheter a password is correct """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
