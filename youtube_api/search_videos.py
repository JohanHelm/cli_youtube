from requests import get
from os.path import expanduser

from youtube_api.api_key import KEY
from exceptions import MyExceptions
from database import Database


# quota cost of 100 unit.
# Поиск видео по id канала и по названию видео


class VideoSearcher:
    __slots__ = ('url', 'nextPageToken', 'prevPageToken', 'part', 'type', 'db', 'exceptions')

    def __init__(self):
        self.url = 'https://youtube.googleapis.com/youtube/v3/search?'
        self.nextPageToken = ''
        self.prevPageToken = ''
        self.part = 'snippet'
        self.type = 'video'
        self.db = Database(f'{expanduser("~")}/cli_youtube/my_favorites.db')
        self.exceptions = MyExceptions()

    def find_channel_videos(self, channel_id: str, page_token: str = ''):
        url = f"{self.url}part={self.part}&type={self.type}&max_results=50&order=date&channelId={channel_id}" \
              f"&key={KEY}&pageToken={page_token}"
        try:
            response = get(url).json()
        except Exception as error:
            self.exceptions.handler(error)
        else:
            self.nextPageToken = response.get('nextPageToken')
            self.prevPageToken = response.get('prevPageToken')
            videos = response['items']
            for video in videos:
                video_info = video['snippet']
                self.db.add_video(video['id']['videoId'], video_info['title'], video_info['description'],
                             video_info['channelTitle'], video_info['publishedAt'],
                             video_info['thumbnails']['default']['url'], video_info['channelId'])

    def next_page(self, search_query: str):
        if self.nextPageToken:
            self.find_channel_videos(search_query, self.nextPageToken)

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.find_channel_videos(search_query, self.prevPageToken)

    def update_channel_videos(self, channel_id: str, page_token: str = ''):
        url = f"{self.url}part={self.part}&type={self.type}&max_results=50&order=date&channelId={channel_id}" \
              f"&key={KEY}&pageToken={page_token}"
        try:
            response = get(url).json()
        except Exception as error:
            self.exceptions.handler(error)
        else:
            self.nextPageToken = response.get('nextPageToken')
            self.prevPageToken = response.get('prevPageToken')
            videos = iter(response['items'])
            del response
            for video in videos:
                video_info = video['snippet']
                if all(self.db.check_video_in_db(video['id']['videoId'])):
                    self.nextPageToken = None
                    self.prevPageToken = None
                    break
                else:
                    self.db.add_video(video['id']['videoId'], video_info['title'], video_info['description'],
                                 video_info['channelTitle'], video_info['publishedAt'],
                                 video_info['thumbnails']['default']['url'], video_info['channelId'])
