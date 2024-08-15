#!/usr/bin/env python3
""" user Module """

from sqlalchemy import Column, VARCHAR, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ User class (users table) """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(250), nullable=False)
    hashed_password = Column(VARCHAR(250), nullable=False)
    session_id = Column(VARCHAR(250), nullable=True)
    reset_token = Column(VARCHAR(250), nullable=True)
