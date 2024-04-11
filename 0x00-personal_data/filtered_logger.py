#!/usr/bin/env python3
""" Regex-ing """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Function that returns the log
    message obfuscated """
    for i in fields:
        message = re.sub(i+'=.*?'+separator,
                         i+'='+redaction+separator, message)
    return message
