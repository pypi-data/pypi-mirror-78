"""Top-level package for Vodafone Ireland Account Checker."""

__author__ = """Finbarr Brady"""
__email__ = 'finbarr.brady@gmail.com'
__version__ = '1.0.7'


import coloredlogs
import os
import logging

format_string = '%(asctime)s,%(msecs)03d ' \
                '%(levelname)8s [%(filename)s:%(lineno)s ' \
                '- %(funcName)18s() ] %(message)s'
formatter = logging.Formatter(format_string)

coloredlogs.install(
    fmt=format_string,
    level=os.getenv("LOG_LEVEL", "DEBUG"))
