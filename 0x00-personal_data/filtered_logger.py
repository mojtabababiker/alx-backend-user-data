#!/usr/bin/env python3
"""
aboduscatation funciton moduel
"""
import re
from typing import Sequence
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence[str]):
        """
        initiate RedactingFormatter instance
        Parameters:
        ------------
        fields: a list of str represents the to be abfuscate
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the record message by removing all the PII entities from
        the record message
        parameters:
        ------------
        record: a logging record with the message to be logged

        Return:
        ------------
        str: the formatted message after removing all the PII
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: Sequence[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filter a log message by obfuscate the sensitive fields on it
    return the new obfuscated message

    Parameters:
    -----------
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
               fields in the log line (message)

    Returns:
    ------------
    str: The obfuscated message
    """
    obf_msg = message

    for field in fields:
        pattern = r"{}=.*?{}".format(field, separator)
        repl = r"{}={}{}".format(field, redaction, separator)
        obf_msg = re.sub(pattern=pattern, repl=repl, string=obf_msg)

    return obf_msg
