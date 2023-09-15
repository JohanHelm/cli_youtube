# from youtube_api import youtube
from database import db
from search_channels import channel_search
from search_playlists import playlist_search
from search_videos import video_search


class YoutubeManager:

    def add_fav_channel(self, selected_item):
        # Достать id канала
        channel_info = db.get_channel_from_temp(selected_item)[1:]
        # скачать инфу о всех видео канала

        # Скачать инфу о всех плейлисах канала и добавить в базу
        for title, description, author, published_at, thumbnails, video_id, channel_id \
                in video_search.find_channel_videos(channel_info[2]):
            db.add_video(title, description, author, published_at, thumbnails, video_id, channel_id)

        for title, description, thumbnails, playist_id, videos in playlist_search.find_playlists(channel_info[2]):
            db.add_playlist(title, description, thumbnails, playist_id, channel_info[2])

        db.add_channel(*channel_info)
        # print(db.get_channel_from_temp(selected_item))
        # print(playlist_search.find_playlists(channel_id))

    def search_channel(self, search_query):
        db.clear_temp_channel()
        channel_search.find_channel(search_query)
        # while channel_search.nextPageToken:
        #     channel_search.next_page(search_query)



yt = YoutubeManager()

# yt.search_channel('python hub studio')
