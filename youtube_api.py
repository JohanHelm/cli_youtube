from googleapiclient.discovery import build
from api_key import KEY


youtube = build('youtube', 'v3', developerKey=KEY)


