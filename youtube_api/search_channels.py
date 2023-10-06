from requests import get
from os.path import expanduser

from youtube_api.api_key import KEY
from exceptions import MyExceptions
from database import Database


# quota cost of 100 unit.
# Поиск канала по имени


class ChannelSearcher:
    __slots__ = ('url', 'nextPageToken', 'prevPageToken', 'part', 'type', 'db', 'exceptions')

    def __init__(self):
        self.url = 'https://youtube.googleapis.com/youtube/v3/search?'
        self.nextPageToken = ''
        self.prevPageToken = ''
        self.part = 'snippet'
        self.type = 'channel'
        self.db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
        self.exceptions = MyExceptions()

    def find_channel(self, search_query: str, page_token: str = ''):
        url = f"{self.url}part={self.part}&type={self.type}&max_results=50&q={search_query}" \
              f"&key={KEY}&pageToken={page_token}"
        try:
            response = get(url).json()
        except Exception as error:
            self.exceptions.handler(error)
        else:
            self.nextPageToken = response.get('nextPageToken')
            self.prevPageToken = response.get('prevPageToken')
            channels = response['items']

            for channel in channels:
                channel_info = channel['snippet']
                self.db.save_temp_channel(channel_info['channelId'], channel_info['channelTitle'],
                                     channel_info['publishedAt'], channel_info['description'],
                                     channel_info['thumbnails']['default']['url'])

    def next_page(self, search_query: str):
        if self.nextPageToken:
            self.find_channel(search_query, self.nextPageToken)

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.find_channel(search_query, self.prevPageToken)
