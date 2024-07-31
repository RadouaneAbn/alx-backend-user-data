#!/usr/bin/env python3
""" filtered_logger module """

from typing import List
import re
import logging
from datetime import datetime


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
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
