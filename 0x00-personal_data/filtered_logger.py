#!/usr/bin/env python3
""" 0. Regex-ing """
import re
import csv
from os import getenv 
import logging
from typing import List
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """
    function that takes no arguments and returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    function that returns a connector to the database object
    """
    db_user = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            database=db_name
            )
    return connection
