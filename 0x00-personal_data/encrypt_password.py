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
