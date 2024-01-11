#!/usr/bin/env python3
'''
    module that handles personal data
'''
import logging
import re
from typing import List


def filter_datum(fields:List[str], redaction: str,
                message:str, separator:str) -> str:
    '''
        function that obfuscates personal information

        Arguments:
        fields: a list of strings representing all fields to
        obfuscate
        redaction: a string representing by what the field will
        be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is
        separating all fields in the log line (message)

        Return: String with redacted values
    '''
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message
