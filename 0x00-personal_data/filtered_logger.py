#!/usr/bin/env python3
""" filtered_logger module """

import re
import logging
import os
from typing import List
import mysql.connector

PII_FIELDS = ("password", "email", "name", "ssn", "phone")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init method """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Format method """
        return filter_datum(
                self.fields,
                self.REDACTION,
                super(RedactingFormatter, self).format(record),
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    This function returns a connector to the database
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(
        user=user,
        password=passwd,
        host=host,
        database=db_name)
    return conn


def main() -> None:
    """ The main function """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]}; ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        logger.info(msg=message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
