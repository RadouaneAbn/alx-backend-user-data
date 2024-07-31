#!/usr/bin/env python3
""" filtered_logger module """

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ This function return a log message obfuscated. """
    pattern = fr'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, rf'\1={redaction}', message)
