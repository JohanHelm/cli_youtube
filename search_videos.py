from googleapiclient.discovery import build
### quota cost of 100 unit. ###

KEY = 'AIzaSyDWO6QmE-DV16-NQ19EYYHxeH1E-xrCu_w'
youtube = build('youtube', 'v3', developerKey=KEY)


# Выполнение запроса к API для поиска каналов/видео

types = ('video', 'channel', 'playlist')
channel_id = 'UCZ26MoNJKaGXFQWKuGVzmAg'
nextPageToken = 'CA8QAA'
response = youtube.search().list(channelId=channel_id, part='snippet', type='video', maxResults=50).execute()

print(response)

# Извлечение информации о найденных видео из ответа API
# videos = response['items']
# for video in videos:
#     print(video)
#     print('--------------')
#     video_info = video['snippet']
#     print('Заголовок видео:', video_info['title'])
#     print('Описание видео:', video_info['description'])
#     print('Автор видео:', video_info['channelTitle'])
#     print('Видео ID:', video['id']['videoId'])
#     print('Картинка:', video_info['thumbnails']['high']['url'])
#     print('ID канала', video_info['channelId'])
#     print('-------------------------------------------')

