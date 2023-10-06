from os import system
from os.path import expanduser

from database import Database
from youtube_api.search_channels import ChannelSearcher
from youtube_api.search_videos import VideoSearcher


def add_fav_channel(page, show_results, selected_item):
    # Get channel_id
    db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
    channel_id = db.show_temp_channels(page, show_results)[0][selected_item][0]
    channel_info = db.get_channel_from_temp(channel_id)
    # add channel if the channel no in db
    if not all(db.check_channel_in_fav(channel_id)):
        db.add_channel(*channel_info)
        # get all channel videos
        video_search = VideoSearcher()
        video_search.find_channel_videos(channel_id)
        while video_search.nextPageToken:
            video_search.next_page(channel_id)

def rm_channel(channel_id):
    db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
    db.rm_channel(channel_id)

def search_channel(search_query):
    db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
    db.clear_temp_channel()
    channel_search = ChannelSearcher()
    channel_search.find_channel(search_query)
    # while channel_search.nextPageToken:
    #     channel_search.next_page(search_query)

def playback_video(page, show_results, selected_item, channel_id):
    db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
    video_id = db.show_channel_videos(page, show_results, channel_id)[0][selected_item][0]
    system(f'mpv -fs https://www.youtube.com/watch?v={video_id}')

def update_channel_videos(channel_id):
    video_search = VideoSearcher()
    video_search.update_channel_videos(channel_id)
    while video_search.nextPageToken:
        video_search.next_page(channel_id)
