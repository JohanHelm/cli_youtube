from youtube_api import youtube
from database import db
from search_playlists import playlist_search


class YoutubeManager:
    def __init__(self, youtube):
        self.youtube = youtube
        # self.nextPageToken = None
        # self.prevPageToken = None
        # self.part = 'snippet'
        # self.type = 'channel'
        # self.page_num = 1

    def add_fav_channel(self, selected_item):
        # Достать id канала
        channel_info = db.get_channel_from_temp(selected_item)[1:]
        # скачать инфу о всех видео канала
        # Скачать инфу о всех плейлисах канала и добавить в базу

        for title, description, thumbnails, playist_id in playlist_search.find_playlists(channel_info[2]):
            db.add_playlist(title, description, thumbnails, playist_id, channel_info[2])
        #
        #


        db.add_channel(*channel_info)
        # print(db.get_channel_from_temp(selected_item))
        # print(playlist_search.find_playlists(channel_id))

yt = YoutubeManager(youtube)
# yt.add_fav_channel(0)


