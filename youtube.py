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
        channel_id = db.get_channel_from_temp(selected_item)[3]
        # скачать инфу о всех видео канала
        # Скачать инфу о всех плейлисах канала и добавить в базу
        for playlist in playlist_search.find_playlists(channel_id):

        # Скачать инфу о всех видео плейлиста
        #


        # db.add_fav_channel(selected_item)
        # print(db.get_channel_from_temp(selected_item))
        print(*)

yt = YoutubeManager(youtube)
yt.add_fav_channel(0)


