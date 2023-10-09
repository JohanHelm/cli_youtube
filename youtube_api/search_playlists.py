import requests
from os.path import expanduser

from youtube_api.api_key import KEY
from exceptions import MyExceptions
from database import Database

# quota cost of 1 unit.
# playlist search by channel id

class PlaylistSearcher:
    __slots__ = ('pl_nextPageToken', 'pl_prevPageToken', 'vi_nextPageToken', 'vi_prevPageToken', 'part',
                 'db', 'exceptions')

    def __init__(self):
        self.pl_nextPageToken = ''
        self.pl_prevPageToken = ''
        self.vi_nextPageToken = ''
        self.vi_prevPageToken = ''
        self.part = 'snippet'
        self.db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
        self.exceptions = MyExceptions()

    def find_channel_playlists(self, channel_id: str, page_token: str = ''):
        basic_url = 'https://www.googleapis.com/youtube/v3/playlists?'
        # basic_url = 'https://youtube.googleapis.com/youtube/v3/playlists?'  # reserve google api url
        url = f"{basic_url}part={self.part}&max_results=50&channelId={channel_id}&key={KEY}&pageToken={page_token}"
        try:
            response = requests.get(url).json()
        except Exception as error:
            self.exceptions.handler(error)
        else:
            self.pl_nextPageToken = response.get('nextPageToken', '')
            self.pl_prevPageToken = response.get('prevPageToken', '')
            playlists = response.get('items', '')
            for playlist in playlists:
                self.db.add_playlist(playlist['id'], playlist['snippet']['title'], playlist['snippet']['publishedAt'],
                                playlist['snippet']['description'], playlist['snippet']['thumbnails']['default']['url'],
                                channel_id)
                self.find_playlist_videos(playlist['id'])
                while self.vi_nextPageToken:
                    self.vi_next_page(playlist['id'])

    def pl_next_page(self, channel_id: str):
        if self.pl_nextPageToken:
            self.find_channel_playlists(channel_id, self.pl_nextPageToken)

    def pl_prev_page(self, channel_id: str):
        if self.pl_prevPageToken:
            self.find_channel_playlists(channel_id, self.pl_prevPageToken)

    def find_playlist_videos(self, playlist_id, page_token: str = ''):
        basic_url = 'https://www.googleapis.com/youtube/v3/playlistItems?'
        # basic_url = 'https://youtube.googleapis.com/youtube/v3/playlistItems?'  # reserve google api url
        url = f"{basic_url}part={self.part}&max_results=50&playlistId={playlist_id}&key={KEY}&pageToken={page_token}"
        try:
            response = requests.get(url).json()
        except Exception as error:
            self.exceptions.handler(error)
        else:
            self.vi_nextPageToken = response.get('nextPageToken', '')
            self.vi_prevPageToken = response.get('prevPageToken', '')
            videos = response.get('items', '')
            for video in videos:
                self.db.mark_videos_in_playlist(playlist_id, video['snippet']['resourceId']['videoId'])

    def vi_next_page(self, playlist_id: str):
        if self.vi_nextPageToken:
            self.find_playlist_videos(playlist_id, self.vi_nextPageToken)

    def vi_prev_page(self, playlist_id: str):
        if self.vi_prevPageToken:
            self.find_playlist_videos(playlist_id, self.vi_prevPageToken)



# ps = PlaylistSearcher()
# # ps.find_channel_playlists('UC5dgoavpIertLkNDDITDoBQ')
# ps.find_playlist_videos('PL5FMLPRj1j6JcmFb0oC7hDycF6nSNRsfl')
