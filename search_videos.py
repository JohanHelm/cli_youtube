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

        found_videos = []
        videos = response['items']
        for num, video in enumerate(videos):
            video_info = video['snippet']


            video_data = (video_info['title'], video_info['description'], video_info['channelTitle'],
                          video_info['publishedAt'], video_info['thumbnails']['default']['url'], video['id']['videoId'],
                          video_info['channelId'])
            found_videos.append(video_data)
        return found_videos


    def next_page(self, search_query: str):
        if self.nextPageToken:
            self.page_num += 1
            self.find_channel_videos(search_query, self.nextPageToken)
        else:
            print('больше каналов нет')

    def prev_page(self, search_query: str):
        if self.prevPageToken:
            self.page_num -= 1
            self.find_channel_videos(search_query, self.prevPageToken)
        else:
            print('больше каналов нет')



video_search = VideoSearcher(youtube)




# channel_id = 'UCN3nx9hIzgItJeDb5FFfy0Q'
#
# c = video_search.find_channel_videos(channel_id)


# Извлечение информации о найденных видео из ответа API
# videos = c['items']
# for video in videos:
#     print(video)
#     print('--------------')
#     video_info = video['snippet']
#     print('Заголовок видео:', video_info['title'])
#     print('Описание видео:', video_info['description'])
#     print('Автор видео:', video_info['channelTitle'])
#     print('Опубликовано:', video_info['publishedAt'])
#     print('Картинка:', video_info['thumbnails']['default']['url'])
#     print('Видео ID:', video['id']['videoId'])
#     print('ID канала', video_info['channelId'])
#     print('-------------------------------------------')

