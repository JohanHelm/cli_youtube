from youtube_api import youtube
from database import db
from pympler import asizeof

# quota cost of 100 unit.
# Поиск видео по id канала и по названию видео


class VideoSearcher:
    __slots__ = ('youtube', 'nextPageToken', 'prevPageToken', 'part', 'type')

    def __init__(self, youtube):
        self.youtube = youtube
        self.nextPageToken = None
        self.prevPageToken = None
        self.part = 'snippet'
        self.type = 'video'

    def find_channel_videos(self, channel_id: str, page_token: str = None):
        response = youtube.search().list(channelId=channel_id, part=self.part, type=self.type, pageToken=page_token,
                                         maxResults=50, order='date').execute()
        self.nextPageToken = response.get('nextPageToken')
        self.prevPageToken = response.get('prevPageToken')
        videos = response['items']
        for num, video in enumerate(videos):
            video_info = video['snippet']
            db.add_video(video['id']['videoId'], video_info['title'], video_info['description'],
                         video_info['channelTitle'], video_info['publishedAt'],
                         video_info['thumbnails']['default']['url'], video_info['channelId'])

    def next_page(self, search_query: str):
        if self.nextPageToken:
            self.find_channel_videos(search_query, self.nextPageToken)
        else:
            print('No more videos.')

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.find_channel_videos(search_query, self.prevPageToken)
        else:
            print('No more videos.')

    def update_channel_videos(self, channel_id: str, page_token: str = None):
        response = youtube.search().list(channelId=channel_id, part=self.part, type=self.type, pageToken=page_token,
                                         maxResults=50, order='date').execute()
        self.nextPageToken = response.get('nextPageToken')
        self.prevPageToken = response.get('prevPageToken')
        videos = response['items']
        for num, video in enumerate(videos):
            video_info = video['snippet']
            if all(db.check_video_in_db(video['id']['videoId'])):
                self.nextPageToken = None
                self.prevPageToken = None
                break
            else:
                db.add_video(video['id']['videoId'], video_info['title'], video_info['description'],
                             video_info['channelTitle'], video_info['publishedAt'],
                             video_info['thumbnails']['default']['url'], video_info['channelId'])

    def find_video_by_title(self, search_query: str, page_token: str = None):
        response = youtube.search().list(q=search_query, part=self.part, type=self.type, pageToken=page_token,
                                         maxResults=50).execute()


video_search = VideoSearcher(youtube)
# print(asizeof.asizeof(video_search))
# 1066800 with __dict__
# 1066128