# gsheets - pythonic wrapper for the google sheets api and some drive api

"""Google docs spreadsheets as Python objects."""

from .api import Sheets
from .oauth2 import get_credentials
from .backend import build_service

__all__ = ['Sheets', 'get_credentials', 'build_service']

__title__ = 'gsheets'
__version__ = '0.5.1'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2016-2020 Sebastian Bank'
