from datetime import datetime

from globals import gp
from googleapiclient.errors import HttpError
from httplib2.error import ServerNotFoundError


def save_to_log(error):
    with open('log_file.txt', 'a', encoding='utf-8') as file:
        file.write(f'\t\t{datetime.now()}\n{error}\n\n')


def exceptions_handler(error):
    save_to_log(error)
    prefix = 'The following error occurred during the last operation:'
    if isinstance(error, HttpError):
        reason = f'{prefix} {error._get_reason()}'
    elif isinstance(error, TimeoutError):
        reason = f'{prefix} Request time exceeded timeout.'
    elif isinstance(error, UnicodeDecodeError):
        reason = 'An error occurred during user input decoding, please repeat your input.'
    elif isinstance(error, OSError):
        reason = 'Network is unreachable. Check your internet connection.'
    elif isinstance(error, ServerNotFoundError):
        reason = f'{error}. Check your internet connection.'
    else:
        reason = 'An error that cannot be handled occurred during the last operation.'
    gp.STATUS_MESSAGE = reason
