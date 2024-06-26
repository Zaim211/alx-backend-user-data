#!/usr/bin/env python3
""" Module for handling Personal Data """
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Function that returns the log
    message obfuscated """
    for i in fields:
        message = re.sub(i+'=.*?'+separator,
                         i+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ redact the message of LogRecord instance """
        message = super(RedactingFormatter, self).format(record)
        red = filter_datum(self.fields, self.REDACTION,
                           message, self.SEPARATOR)
        return red


def get_logger() -> logging.Logger:
    """ Function that takes no arguments and returns
    a logging.Logger object """
    # Create logger
    logger = logging.getLogger('user_data')

    # Set level
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create handler
    handler = logging.StreamHandler()

    # Set formatter as RedactingFormatter
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Function that returns a connector to the database """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    passd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    cn = mysql.connector.connect(user=user,
                                 password=passd,
                                 host=host,
                                 database=db_name)
    return cn


def main():
    """
    main Function should run when the module is executed
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for x in cursor:
        message = "".join("{}={}; ".format(i, j) for i, j in zip(fields, x))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
