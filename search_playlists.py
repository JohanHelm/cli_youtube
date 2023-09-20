from database import db
from youtube_api import youtube


# Поиск плейлистов канала
# quota cost of 1 unit.


class PaylistsSearcher:
    def __init__(self, youtube):
        self.youtube = youtube
        self.pl_nextPageToken = None
        self.pl_prevPageToken = None
        self.vi_nextPageToken = None
        self.vi_prevPageToken = None
        self.part = 'snippet'
        self.pl_page_num = 1
        self.vi_page_num = 1

    def find_playlists(self, channel_id: str, page_token: str = None):
        response = self.youtube.playlists().list(part=self.part, channelId=channel_id, maxResults=50,
                                                 pageToken=page_token).execute()
        self.pl_nextPageToken = response.get('nextPageToken')
        self.pl_prevPageToken = response.get('prevPageToken')
        playlists = response['items']
        for playlist in playlists:
            db.add_playlist(playlist['id'], playlist['snippet']['title'], playlist['snippet']['publishedAt'],
                            playlist['snippet']['description'], playlist['snippet']['thumbnails']['default']['url'],
                            channel_id)
            self.find_pl_videos(playlist['id'])
            while self.vi_nextPageToken:
                self.vi_next_page(playlist['id'])

    def pl_next_page(self, channel_id: str):
        if self.pl_nextPageToken:
            self.pl_page_num += 1
            self.find_playlists(channel_id, self.pl_nextPageToken)
        else:
            print('No more playlists.')

    def pl_prev_page(self, channel_id: str):
        if self.pl_prevPageToken:
            self.pl_page_num -= 1
            self.find_playlists(channel_id, self.pl_prevPageToken)
        else:
            print('No more playlists.')

    def find_pl_videos(self, playlist_id, page_token: str = None):
        response = youtube.playlistItems().list(part=self.part, playlistId=playlist_id, maxResults=50,
                                                pageToken=page_token).execute()
        self.vi_nextPageToken = response.get('nextPageToken')
        self.vi_prevPageToken = response.get('prevPageToken')
        for video in response['items']:
            db.mark_videos_in_playlist(playlist_id, video['snippet']['resourceId']['videoId'])

    def vi_next_page(self, playlist_id: str):
        if self.vi_nextPageToken:
            self.vi_page_num += 1
            self.find_pl_videos(playlist_id, self.vi_nextPageToken)
        else:
            print('No more videos.')

    def vi_prev_page(self, playlist_id: str):
        if self.vi_prevPageToken:
            self.vi_page_num -= 1
            self.find_pl_videos(playlist_id, self.vi_prevPageToken)
        else:
            print('No more videos.')


playlist_search = PaylistsSearcher(youtube)

# channel_id = 'UCN3nx9hIzgItJeDb5FFfy0Q'
# playlist_search.find_playlists(channel_id)
# playlist_search.find_pl_videos('PLNi5HdK6QEmWdZmDJM0Yb6qEGepZhsJQL')
