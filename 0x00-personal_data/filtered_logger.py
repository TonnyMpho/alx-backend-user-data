#!/usr/bin/env python3
""" 0. Regex-ing """
import re
import logging
from typing import List


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
        """
        method to filter values in incoming log records using filter_datum
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION, message,
                                self.SEPARATOR)
        return redacted


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    function that returns the log message obfuscated:
    ------------------
    Arguments
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating
    all fields in the log line (message)
    """
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  f'\\1={redaction}', message)
