#!/usr/bin/env python3
"""
aboduscatation funciton moduel
"""
import logging
import os
import re
from typing import List
import mysql.connector


PII_FIELDS = ("email", "phone", "ssn", "name", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
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


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filter a log message by obfuscate the sensitive fields on it"""
    pattern = r"(?P<f>{})=.*?{}".format('|'.join(fields), separator)
    return re.sub(pattern, repl=r"\g<f>={}{}".format(redaction, separator),
                  string=message)


def get_logger() -> logging.Logger:
    """
    create a new logger and returns it
    """
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_data = logging.getLogger("user_data")
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    user_data.addHandler(handler)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connect to a database using enviornment variable and return
    a connector object
    """
    user_name = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        user=user_name,
        password=password,
        host=host,
        database=db_name
        )
    return db
