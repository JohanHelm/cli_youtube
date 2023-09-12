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
        playlists = response['items']
        # print(response)
        result = []
        for playlist in playlists:
            response2 = youtube.playlistItems().list(part='snippet', playlistId=playlist['id'], maxResults=50,
                                                     pageToken=None).execute()
            videos_in_playlist = tuple([item['snippet']['resourceId']['videoId'] for item in response2['items']])

            result.append((playlist['snippet']['title'], playlist['snippet']['description'],
                           playlist['snippet']['thumbnails']['default']['url'], playlist['id'], videos_in_playlist))
        return result



channel_id = 'UCN3nx9hIzgItJeDb5FFfy0Q'
playlist_search = PaylistsSearcher(youtube)

# c = playlist_search.find_playlists(channel_id)
# #
# for playlist in c:
#     # print(title, description, thumbnails, playist_id, videos)
#     print(playlist)
#     print('---------------------')

