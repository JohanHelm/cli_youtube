from os import system
from os.path import expanduser

from database import Database
from youtube_api.search_channels import ChannelSearcher
from youtube_api.search_videos import VideoSearcher
from youtube_api.search_playlists import PlaylistSearcher


class YoutubeManager:
    __slots__ = ('db', 'video_search', 'playlist_search', 'channel_search')

    def __init__(self):
        self.db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
        self.video_search = VideoSearcher()
        self.playlist_search = PlaylistSearcher()
        self.channel_search = ChannelSearcher()

    def add_fav_channel(self, page, show_results, selected_item):
        # Get channel_id
        channel_id = self.db.show_temp_channels(page, show_results)[0][selected_item][0]
        channel_info = self.db.get_channel_from_temp(channel_id)
        # add channel if the channel no in db
        if not all(self.db.check_channel_in_fav(channel_id)):
            self.db.add_channel(*channel_info)
            # get all channel videos
            self.video_search.find_channel_videos(channel_id)
            while self.video_search.nextPageToken:
                self.video_search.next_page(channel_id)
            # get all channel playlists
            self.playlist_search.find_channel_playlists(channel_id)
            while self.playlist_search.pl_nextPageToken:
                self.playlist_search.pl_next_page(channel_id)

    def rm_channel(self, channel_id):
        self.db.rm_channel(channel_id)

    def search_channel(self, search_query):
        self.db.clear_temp_channel()
        self.channel_search.find_channel(search_query)
        # while channel_search.nextPageToken:
        #     channel_search.next_page(search_query)

    def update_channel_data(self, channel_id):
        self.video_search.update_channel_videos(channel_id)
        while self.video_search.nextPageToken:
            self.video_search.next_page(channel_id)
        self.playlist_search.find_channel_playlists(channel_id)
        while self.playlist_search.pl_nextPageToken:
            self.playlist_search.pl_next_page(channel_id)

    def playback_channel_video(self, page, show_results, selected_item, channel_id):
        video_id = self.db.show_channel_videos(page, show_results, channel_id)[0][selected_item][0]
        system(f'mpv -fs https://www.youtube.com/watch?v={video_id}')

    def playback_playlist_video(self, page, show_results, selected_item, playlist_id):
        video_id = self.db.show_playlist_videos(page, show_results, playlist_id)[0][selected_item][0]
        system(f'mpv -fs https://www.youtube.com/watch?v={video_id}')
