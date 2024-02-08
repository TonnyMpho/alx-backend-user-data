#!/usr/bin/env python3
""" 0. Regex-ing """
import re
import logging


def filter_datum(fields, redaction, message, separator):
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
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+', f'\\1={redaction}', message)
