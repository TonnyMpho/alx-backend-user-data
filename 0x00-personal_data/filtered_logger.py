#!/usr/bin/env python3
""" 0. Regex-ing """
import re
import logging
from typing import List


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
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+', f'\\1={redaction}', message)
