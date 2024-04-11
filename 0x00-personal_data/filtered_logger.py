#!/usr/bin/env python3
""" Regex-ing """
from typing import List
import re
import logging


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
