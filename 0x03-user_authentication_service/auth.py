#!/usr/bin/env python3
""" auth Module """
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ This function return a hashed password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register a new user or raise ValueError if user
            email is already registered """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password).decode()
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ This method validate a user """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(),
                              user.hashed_password.encode()):
                return True
        except NoResultFound:
            pass
        return False
