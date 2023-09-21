from collections import namedtuple

from api_key import KEY

MenuItem = namedtuple('MenuItem', ('message', 'choices', 'demand_user_input'), defaults=(False,))

main_menu = MenuItem('Hi, this is YOUTUBE command line client.',
                     ('Find video.', 'Find channel.', 'My favorites.', 'YOUTUBE API KEY.', 'Exit.'))

find_video = MenuItem('Type video title.', ('Back to Main menu.', 'Exit.'), True)

find_channel = MenuItem('Type channel title.', ('Back to Main menu.', 'Exit.'), True)

my_favorite = MenuItem('My favorite channels.', ('Back to Main menu.', 'Exit.'))

youtube_api_key = MenuItem('This application needs YouTube API key.',
                           ('Add YouTube API key.', 'How to add YouTube API key.', 'Back to Main menu.', 'Exit.'))

add_api_key = MenuItem(f'1. Copy your YouTube API key.\n'
                       f'2. Press Enter before pasting the key.\n'
                       f'3. Paste the key using Ctrl+C+V, then press Enter.\n'
                       f'4. Ensure that the key matches.\n'
                       f"5. If you don't want to change your key, leave the input field empty and press Enter.\n"
                       f'Your youtube api key: {KEY}', ('Back to YOUTUBE API KEY.', 'Exit.'), True)

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

found_channes = MenuItem('Choose channel and press enter to add it in favorites.',
                         ('Back to Main menu.', 'Exit.'))

channel_data = MenuItem('', ('Remove from favorites.', 'Videos.', 'Playlists.',
                             'Back to My favorites.', 'Exit.'))

channel_videos = MenuItem('Choose video and press enter for playback.',
                          ('Back to Channel data.', 'Exit.'))

channel_playlists = MenuItem('Chose playlist and press enter to open playlist summary.',
                             ('Back to Channel data.', 'Exit.'))

menu = {'Main menu.': main_menu,
        'Find video.': find_video,
        'Find channel.': find_channel,
        'My favorites.': my_favorite,
        'YOUTUBE API KEY.': youtube_api_key,
        'Add YouTube API key.': add_api_key,
        'How to add YouTube API key.': how_to_add_api_key,
        'Found channels.': found_channes,
        'Channel data.': channel_data,
        'Videos.': channel_videos,
        'Playlists.': channel_playlists
        }
