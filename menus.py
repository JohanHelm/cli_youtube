from collections import namedtuple

from api_key import KEY
from database import db
from globals import gp
from youtube import yt


def pagination(pages, responce_data):
    gp.RESULTS_AMOUNT = len(responce_data)
    result = [' '.join(i[1:]) for i in responce_data]
    if gp.PAGE < pages:
        result.append('Forward.')
    if gp.PAGE > 1:
        result.append('Back.')
    return result


def options_my_favorite():
    my_channels_data, pages = db.show_my_channels(gp.PAGE, gp.SHOW_RESULTS)
    options = pagination(pages, my_channels_data)
    options.extend(['Back to Main menu.', 'Exit.'])
    return options


def options_found_channels():
    found_channels_data, pages = db.show_temp_channels(gp.PAGE, gp.SHOW_RESULTS)
    options = pagination(pages, found_channels_data)
    options.extend(['Back to Main menu.', 'Exit.'])
    return options


def options_channel_videos():
    channel_videos_data, pages = db.show_channel_videos(gp.PAGE, gp.SHOW_RESULTS, gp.CHANNEL_ID)
    options = pagination(pages, channel_videos_data)
    options.extend(['Back to Channel data.', 'Exit.'])
    return options


def channel_data_text():
    gp.CHANNEL_ID, *chosen_channel_data = db.show_my_channels(gp.PAGE, gp.SHOW_RESULTS)[0][gp.ITEM_TO_SHOW]
    return ' '.join(chosen_channel_data)


def common_handler(menu_items):
    if menu_items[gp.SELECTED_ITEM] == 'Forward.':
        gp.PAGE += 1
    elif menu_items[gp.SELECTED_ITEM] == 'Back.':
        gp.PAGE -= 1
    elif menu_items[gp.SELECTED_ITEM].startswith('Back to '):
        gp.MENU_LEVEL = menu_items[gp.SELECTED_ITEM].replace('Back to ', '')
        gp.USER_INPUT = None
        gp.PAGE = 1
    elif menu_items[gp.SELECTED_ITEM] == 'Remove from favorites.':
        gp.MENU_LEVEL = 'My favorites.'
        yt.rm_channel(gp.CHANNEL_ID)
    elif menu_items[gp.SELECTED_ITEM] == 'Update the list of video.':
        yt.update_channel_videos(gp.CHANNEL_ID)
    else:
        gp.MENU_LEVEL = menu_items[gp.SELECTED_ITEM]


def add_channel(menu_items):
    if gp.SELECTED_ITEM < gp.RESULTS_AMOUNT:
        yt.add_fav_channel(gp.PAGE, gp.SHOW_RESULTS, gp.SELECTED_ITEM)
    else:
        common_handler(menu_items)


def show_channel(menu_items):
    if gp.SELECTED_ITEM < gp.RESULTS_AMOUNT:
        gp.MENU_LEVEL = 'Channel data.'
        gp.ITEM_TO_SHOW = gp.SELECTED_ITEM
    else:
        common_handler(menu_items)


def playback_video(menu_items):
    if gp.SELECTED_ITEM < gp.RESULTS_AMOUNT:
        gp.ITEM_TO_SHOW = gp.SELECTED_ITEM
        yt.playback_video(gp.PAGE, gp.SHOW_RESULTS, gp.SELECTED_ITEM, gp.CHANNEL_ID)
    else:
        common_handler(menu_items)


MenuItem = namedtuple('MenuItem', ('message', 'choices', 'choice_handler', 'demand_user_input'),
                      defaults=(common_handler, False))

main_menu = MenuItem('Hi, this is YOUTUBE command line client.',
                     ('Find video.', 'Find channel.', 'My favorites.', 'YOUTUBE API KEY.', 'Exit.'))

find_video = MenuItem('Type video title.', ('Back to Main menu.', 'Exit.'), common_handler, True)

find_channel = MenuItem('Type channel title.', ('Back to Main menu.', 'Exit.'), common_handler, True)

my_favorite = MenuItem('My favorite channels.', options_my_favorite, show_channel)

youtube_api_key = MenuItem('This application needs YouTube API key.',
                           ('Add YouTube API key.', 'How to add YouTube API key.', 'Back to Main menu.', 'Exit.'))

add_api_key = MenuItem(f'1. Copy your YouTube API key.\n'
                       f'2. Press Enter before pasting the key.\n'
                       f'3. Paste the key using Ctrl+C+V, then press Enter.\n'
                       f'4. Ensure that the key matches.\n'
                       f"5. If you don't want to change your key, leave the input field empty and press Enter.\n"
                       f'Your youtube api key: {KEY}', ('Back to YOUTUBE API KEY.', 'Exit.'), common_handler, True)

how_to_get_api_key_msg = f'1. Go to https://console.developers.google.com/\n ' \
                         f'2. Create a new project or select an existing one.\n ' \
                         f'3. In the left navigation menu, select "APIs & Services" > "Library."\n ' \
                         f'4. Find and enable the "YouTube Data API v3."\n ' \
                         f'5. In the left navigation menu, select "APIs & Services" > "Credentials."\n ' \
                         f'6. Click on "Create Credentials" and choose the credential type that suits your ' \
                         f'application\n ' \
                         f'(e.g., OAuth 2.0 Client ID for a web application).\n ' \
                         f'7. Follow the on-screen instructions to complete the credentials creation process.\n ' \
                         f'8. click "Download" next to the credentials to obtain a JSON file containing the ' \
                         f'credentials.\n ' \
                         f'9. This application demand api_key'

how_to_add_api_key = MenuItem(how_to_get_api_key_msg, ('Back to YOUTUBE API KEY.', 'Exit.'))

found_channels = MenuItem('Choose channel and press enter to add it in favorites.', options_found_channels, add_channel)

channel_data = MenuItem(channel_data_text, ('Remove from favorites.', 'Update the list of video.', 'Videos.',
                                            'Back to My favorites.', 'Exit.'))

channel_videos = MenuItem('Choose video and press enter for playback.', options_channel_videos, playback_video)

check_updates = MenuItem(f'Current version {gp.VERSION}', ('Check for updates.', 'Back to Main menu.', 'Exit.'))

menus = {'Main menu.': main_menu,
         'Find video.': find_video,
         'Find channel.': find_channel,
         'My favorites.': my_favorite,
         'YOUTUBE API KEY.': youtube_api_key,
         'Check updates.': check_updates,
         'Add YouTube API key.': add_api_key,
         'How to add YouTube API key.': how_to_add_api_key,
         'Found channels.': found_channels,
         'Channel data.': channel_data,
         'Videos.': channel_videos,
         }
