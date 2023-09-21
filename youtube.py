from os import system
from database import db
from search_channels import channel_search
from search_playlists import playlist_search
from search_videos import video_search


class YoutubeManager:

    def add_fav_channel(self, page, show_results, selected_item):
        # Достать id канала
        channel_id = db.show_temp_channels(page, show_results)[0][selected_item][0]
        channel_info = db.get_channel_from_temp(channel_id)
        # print(channel_info)
        # добавить канал если его нет
        if not all(db.check_channel_in_fav(channel_id)):
            db.add_channel(*channel_info)
            # скачать инфу о всех видео канала
            video_search.find_channel_videos(channel_id)
            while video_search.nextPageToken:
                video_search.next_page(channel_id)
            # Скачать инфу о всех плейлисах канала и добавить в базу
            playlist_search.find_playlists(channel_id)
            while playlist_search.pl_nextPageToken:
                playlist_search.pl_next_page(channel_id)

    def rm_channel(self, channel_id):
        db.rm_channel(channel_id)

    def search_channel(self, search_query):
        db.clear_temp_channel()
        channel_search.find_channel(search_query)
        # while channel_search.nextPageToken:
        #     channel_search.next_page(search_query)

    def playback_video(self, page, show_results, selected_item, channel_id):
        video_id = db.show_channel_videos(page, show_results, channel_id)[0][selected_item][0]
        system(f'mpv -fs https://www.youtube.com/watch?v={video_id}')


yt = YoutubeManager()

# yt.search_channel('python hub studio')
# yt.add_fav_channel(1, 5, 0)
# yt.playback(1, 5, 0, 'UCIyLQ6cL0eWj1jT6oyy148w')
