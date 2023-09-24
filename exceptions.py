from globals import gp
from googleapiclient.errors import HttpError
from datetime import datetime


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
        reason = f'An error occurred during user input decoding, please repeat your input.'
    else:
        reason = 'An error that cannot be handled occurred during the last operation.'
    gp.STATUS_MESSAGE = reason


# TimeoutError:                                     Превышение таймаута по запросу
# UnicodeDecodeError:                               Ошибка с кодировкой при пользовательском вводе
# OSError: [Errno 101] Network is unreachable       Нет интернета
# http.client.RemoteDisconnected: Remote end closed connection without response       Медленный интернет
# raise ServerNotFoundError("Unable to find the server at %s" % conn.host)
# httplib2.error.ServerNotFoundError: Unable to find the server at youtube.googleapis.com           Не может достучаться до сервера

# raise HttpError(resp, content, uri=self.uri)
# googleapiclient.errors.HttpError: <HttpError 400 when requesting https://youtube.googleapis.com/youtube/v3/search?part=snippet&type=channel&q=Sergey+Nemchinskiy&maxResults=50&key=AIzaSyDWO6QmE-DV16-NQ19EYYHxeH1E-xrCu_w+000&alt=json returned "API key not valid. Please pass a valid API key.". Details: "[{'message': 'API key not valid. Please pass a valid API key.', 'domain': 'global', 'reason': 'badRequest'}]">
