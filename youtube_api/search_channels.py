from database import db
from youtube_api.api_connect import youtube
from exceptions import exceptions

# quota cost of 100 unit.
# Поиск канала по имени


class ChannelSearcher:
    __slots__ = ('youtube', 'nextPageToken', 'prevPageToken', 'part', 'type')

    def __init__(self, youtube):
        self.youtube = youtube
        self.nextPageToken = None
        self.prevPageToken = None
        self.part = 'snippet'
        self.type = 'channel'

    def find_channel(self, search_query: str, page_token: str = None):
        try:
            response = self.youtube.search().list(part=self.part, type=self.type, pageToken=page_token, q=search_query,
                                                  maxResults=50).execute()
        except Exception as error:
            exceptions.handler(error)
        else:
            self.nextPageToken = response.get('nextPageToken')
            self.prevPageToken = response.get('prevPageToken')
            channels = iter(response['items'])
            del response
            for channel in channels:
                channel_info = channel['snippet']
                db.save_temp_channel(channel_info['channelId'], channel_info['channelTitle'],
                                     channel_info['publishedAt'], channel_info['description'],
                                     channel_info['thumbnails']['default']['url'])

    def next_page(self, search_query: str):
        if self.nextPageToken:
            self.find_channel(search_query, self.nextPageToken)

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.find_channel(search_query, self.prevPageToken)


channel_search = ChannelSearcher(youtube)
