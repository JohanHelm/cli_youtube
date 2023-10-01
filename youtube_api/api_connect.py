from googleapiclient.discovery import build

from youtube_api.api_key import KEY


youtube = build('youtube', 'v3', developerKey=KEY)
