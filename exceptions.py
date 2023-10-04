from datetime import datetime

from googleapiclient.errors import HttpError
from httplib2.error import ServerNotFoundError


class MyExceptions:
    __slots__ = ('reason',)

    def __init__(self):
        self.reason = ''

    @staticmethod
    def save_to_log(error):
        with open('log_file.txt', 'a', encoding='utf-8') as file:
            file.write(f'\t\t{datetime.now()}\n{error}\n\n')

    def handler(self, error):
        self.save_to_log(error)
        prefix = 'The following error occurred during the last operation:'
        if isinstance(error, HttpError):
            self.reason = f'{prefix} {error._get_reason()}'
        elif isinstance(error, TimeoutError):
            self.reason = f'{prefix} Request time exceeded timeout.'
        elif isinstance(error, UnicodeDecodeError):
            self.reason = 'An error occurred during user input decoding, please repeat your input.'
        elif isinstance(error, OSError):
            self.reason = 'Network is unreachable. Check your internet connection.'
        elif isinstance(error, ServerNotFoundError):
            self.reason = f'{error}. Check your internet connection.'
        else:
            self.reason = 'An error that cannot be handled occurred during the last operation.'


exceptions = MyExceptions()
