from database import db
from youtube_api import youtube


# quota cost of 100 unit.
# Поиск канала по имени


class ChannelSearcher:
    def __init__(self, youtube):
        self.youtube = youtube
        self.nextPageToken = None
        self.prevPageToken = None
        self.part = 'snippet'
        self.type = 'channel'
        self.page_num = 1

    def find_channel(self, search_query: str, page_token: str = None):
        response = self.youtube.search().list(part=self.part, type=self.type, pageToken=page_token,
                                              q=search_query, maxResults=50).execute()
        self.nextPageToken = response.get('nextPageToken')
        self.prevPageToken = response.get('prevPageToken')
        channels = response['items']
        for num, channel in enumerate(channels):
            channel_info = channel['snippet']
            db.save_temp_channel(channel_info['channelId'], channel_info['channelTitle'],
                                 channel_info['publishedAt'], channel_info['description'],
                                 channel_info['thumbnails']['default']['url'])

    def next_page(self, search_query: str):
        if self.nextPageToken:
            self.page_num += 1
            self.find_channel(search_query, self.nextPageToken)
        else:
            print('No more channels.')

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.page_num -= 1
            self.find_channel(search_query, self.prevPageToken)
        else:
            print('No more channels.')


# Выполнение запроса к API для поиска канала по имени
# search_query = 'Легенарные бои'

channel_search = ChannelSearcher(youtube)
# print(channel_search.find_channel(search_query))
# channel_search.next_page(search_query)
# channel_search.prev_page(search_query)
