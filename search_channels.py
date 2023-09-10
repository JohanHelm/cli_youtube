from youtube_api import youtube
from database import db

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
                                              q=search_query, maxResults=5).execute()
        self.nextPageToken = response.get('nextPageToken')
        self.prevPageToken = response.get('prevPageToken')
        db.clear_temp_channel()
        found_channels = []
        channels = response['items']
        for num, channel in enumerate(channels):
            channel_info = channel['snippet']
            db.save_temp_channel(num, channel_info['channelTitle'], channel_info['publishedAt'], channel_info['channelId'], channel_info['description'], channel_info['thumbnails']['default']['url'])
            channel_data = f"Канал: {channel_info['channelTitle']} {channel_info['publishedAt']} {channel_info['description'][:100]}"
            found_channels.append(channel_data)
        return found_channels


    def next_page(self, search_query: str):
        if self.nextPageToken:
            self.page_num += 1
            self.find_channel(search_query, self.nextPageToken)
        else:
            print('больше каналов нет')

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.page_num -= 1
            self.find_channel(search_query, self.prevPageToken)
        else:
            print('больше каналов нет')


# Выполнение запроса к API для поиска канала по имени
# search_query = 'Легенарные бои'

channel_search = ChannelSearcher(youtube)
# print(channel_search.find_channel(search_query))
# channel_search.next_page(search_query)
# channel_search.prev_page(search_query)
