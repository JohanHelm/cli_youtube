from youtube_api import youtube
from database import db

# quota cost of 100 unit.
# Поиск видео по id канала и по названию видео


class VideoSearcher:
    def __init__(self, youtube):
        self.youtube = youtube
        self.nextPageToken = None
        self.prevPageToken = None
        self.part = 'snippet'
        self.type = 'video'
        self.page_num = 1

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
            self.page_num += 1
            self.find_channel_videos(search_query, self.nextPageToken)
        else:
            print('No more videos.')

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.page_num -= 1
            self.find_channel_videos(search_query, self.prevPageToken)
        else:
            print('No more videos.')


video_search = VideoSearcher(youtube)
