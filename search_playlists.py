from youtube_api import youtube

# Поиск плейлистов канала
# quota cost of 1 unit.


class PaylistsSearcher:
    def __init__(self, youtube):
        self.youtube = youtube
        self.nextPageToken = None
        self.prevPageToken = None
        self.part = 'snippet'
        self.page_num = 1

    def find_playlists(self, channel_id: str, page_token: str = None):
        response = self.youtube.playlists().list(part=self.part, channelId=channel_id, maxResults=50,
                                            pageToken=page_token).execute()

        # print(response)
        playlists = response['items']

        return ((playlist['snippet']['title'], playlist['snippet']['description'], playlist['snippet']['thumbnails'], playlist['id']) for playlist in playlists)
        # :
        #     playlist_info = playlist['snippet']
        #     print('Заголовок плейлиста:', playlist_info['title'])
        #     print('Описание:', playlist_info['description'])
        #     print('Картинка:', playlist_info['thumbnails'])
        #     print('Идентификатор плейлиста:', playlist['id'])
        #     print('Количество видео:', playlist['contentDetails']['itemCount'])
        #     print('-------------------------------------------')


# channel_id = 'UCN3nx9hIzgItJeDb5FFfy0Q'
playlist_search = PaylistsSearcher(youtube)
# playlist_search.find_playlists(channel_id)

