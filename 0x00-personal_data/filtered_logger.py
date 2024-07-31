#!/usr/bin/env python3
""" filtered_logger module """

from typing import List
import re
import logging

PII_FIELDS = ("password", "email", "name", "ssn", "phone")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format method """
        return filter_datum(
                self.fields,
                self.REDACTION,
                super().format(record),
                self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ This function return a log message obfuscated. """
    pattern = fr'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, rf'\1={redaction}', message)


def get_logger() -> logging.Logger:
    """ This function return a logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger
