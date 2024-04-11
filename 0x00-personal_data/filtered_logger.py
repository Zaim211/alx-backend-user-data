#!/usr/bin/env python3
""" Module for handling Personal Data """
from typing import List
import re
import logging

# Personally identifiable information (PII)
PII_FIELDS = ('name', 'eamil', 'phone', 'ssn', 'password')


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

    # Create stream handler
    stream_handler = logging.StreamHandler()

    # Set formatter as RedactingFormatter
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    # Add the handler to logger
    logger.addHandler(stream_handler)

    # Return logger
    return logger
