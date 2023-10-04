import youtube as yt
from database import db
from settings import settings
from youtube_api.api_key import KEY


class MenuGenerator:
    __slots__ = ('demand_user_input',)

    def __init__(self, demand_user_input=False):
        self.demand_user_input = demand_user_input

    @staticmethod
    def pagination(pages: int, responce_data: tuple, page: int) -> tuple[list, int]:
        results_amount = len(responce_data)
        result = [' '.join(i[1:]) for i in responce_data]
        if page < pages:
            result.append('Forward.')
        if page > 1:
            result.append('Back.')
        return result, results_amount

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        """
        Creates menu message
        Get channel_id
        :return: channel_id, message
        """

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        """
        Create menu options
        save options amount in results_amount
        :return: options, results_amount
        """

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: int, user_input: str,
                       status_message: str, results_amount: int, channel_id: str, item_to_show: int)\
            -> tuple[str, int, str, str, int]:
        """
        Takes user choice and executes further actions
        :return: tuple[str, int, str, str, int]
        """
        if menu_items(selected_item).name == 'Forward.':
            page += 1
        elif menu_items(selected_item).name == 'Back.':
            page -= 1
        elif selected_item == len(menu_items) - 1:  # 'Exit.'
            quit(0)
        elif menu_items(selected_item).name.startswith('Back to ') and menu_level != 'Videos.':
            menu_level = menu_items(selected_item).name.replace('Back to ', '')
        else:
            menu_level = menu_items(selected_item).name

        return menu_level, page, user_input, status_message, item_to_show


class MainMenu(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = 'Hi, this is YOUTUBE command line client.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Find channel.', 'My favorites.', 'YOUTUBE API KEY.', 'Exit.')
        return options, 0


class FindChannel(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__(True)

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = 'Type channel title.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Back to Main menu.', 'Exit.')
        return options, 0

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: int, user_input: str,
                       status_message: str, results_amount: int, channel_id: str, item_to_show: int) \
            -> tuple[str, int, str, str, int]:
        if user_input:
            yt.search_channel(user_input)
            menu_level = 'Found channels.'
            user_input = ''
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, channel_id, item_to_show)
        return menu_level, page, user_input, status_message, 0


class MyFavotrite(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = 'My favorite channels.'
        return channel_id, message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple[list, int]:
        my_channels_data, pages = db.show_my_channels(page, show_results)
        options, results_amount = MenuGenerator.pagination(pages, my_channels_data, page)
        options.extend(['Back to Main menu.', 'Exit.'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: int, user_input: str,
                       status_message: str, results_amount: int, channel_id: str, item_to_show: int) \
            -> tuple[str, int, str, str, int]:
        if selected_item < results_amount:
            menu_level = 'Channel data.'
            item_to_show = selected_item
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, channel_id, item_to_show)
        return menu_level, page, user_input, status_message, item_to_show


class YotubeApiKey(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = 'This application needs YouTube API key.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Add YouTube API key.', 'How to add YouTube API key.', 'Back to Main menu.', 'Exit.')
        return options, 0


class AddApiKey(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__(True)

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = f'1. Copy your YouTube API key.\n' \
                  f'2. Press Enter before pasting the key.\n' \
                  f'3. Paste the key using Ctrl+C+V, then press Enter.\n' \
                  f'4. Ensure that the key matches.\n' \
                  f"5. If you don't want to change your key, leave the input field empty and press Enter.\n" \
                  f'Your youtube api key: {KEY}'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Back to YOUTUBE API KEY.', 'Exit.')
        return options, 0

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: int, user_input: str,
                       status_message: str, results_amount: int, channel_id: str, item_to_show: int) \
            -> tuple[str, int, str, str, int]:
        if user_input:
            with open('api_key.py', 'w', encoding='utf-8') as file:
                file.write(f'KEY = "{user_input}"')
            user_input = ''
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, channel_id, item_to_show)
        return menu_level, page, user_input, status_message, 0


class HowToAddApiKey(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = f'1. Go to https://console.developers.google.com/\n ' \
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
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Back to YOUTUBE API KEY.', 'Exit.')
        return options, 0


class FoundChannels(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = 'Choose channel and press enter to add it in favorites.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple[list, int]:
        found_channels_data, pages = db.show_temp_channels(page, show_results)
        options, results_amount = MenuGenerator.pagination(pages, found_channels_data, page)
        options.extend(['Back to Main menu.', 'Exit.'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: int, user_input: str,
                       status_message: str, results_amount: int, channel_id: str, item_to_show: int) \
            -> tuple[str, int, str, str, int]:
        if selected_item < results_amount:
            yt.add_fav_channel(page, settings.SHOW_RESULTS, selected_item)
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, channel_id, item_to_show)
        return menu_level, page, user_input, status_message, item_to_show


class ChannelData(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        channel_id, *chosen_channel_data = db.show_my_channels(page, show_results)[0][item_to_show]
        return channel_id, ' '.join(chosen_channel_data)

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Remove from favorites.', 'Update the list of video.', 'Videos.', 'Back to My favorites.', 'Exit.')
        return options, 0

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: int, user_input: str,
                       status_message: str, results_amount: int, channel_id: str, item_to_show: int) \
            -> tuple[str, int, str, str, int]:
        if selected_item == 0:
            menu_level = 'My favorites.'
            yt.rm_channel(channel_id)
        elif selected_item == 1:
            yt.update_channel_videos(channel_id)
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, channel_id, item_to_show)
        return menu_level, page, user_input, status_message, item_to_show


class BackToChannel(ChannelData):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        back_channel_data = db.show_back_channel(channel_id)[1:]
        return channel_id, ' '.join(back_channel_data)


class ChannelVideos(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, channel_id: str) -> tuple[str, str]:
        message = 'Choose video and press enter for playback.'
        return channel_id, message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple[list, int]:
        channel_videos_data, pages = db.show_channel_videos(page, show_results, channel_id)
        options, results_amount = MenuGenerator.pagination(pages, channel_videos_data, page)
        options.extend(['Back to Channel data.', 'Exit.'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: int, user_input: str,
                       status_message: str, results_amount: int, channel_id: str, item_to_show: int) \
            -> tuple[str, int, str, str, int]:

        if selected_item < results_amount:
            item_to_show = selected_item
            yt.playback_video(page, settings.SHOW_RESULTS, selected_item, channel_id)
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, channel_id, item_to_show)
        return menu_level, page, user_input, status_message, item_to_show


main_menu = MainMenu()
find_channel = FindChannel()
my_favorite = MyFavotrite()
youtube_api_key = YotubeApiKey()
add_api_key = AddApiKey()
how_to_add_api_key = HowToAddApiKey()
found_channels = FoundChannels()
channel_data = ChannelData()
channel_videos = ChannelVideos()
back_to_channel_data = BackToChannel()

menus = {'Main menu.': main_menu,
         'Find channel.': find_channel,
         'My favorites.': my_favorite,
         'YOUTUBE API KEY.': youtube_api_key,
         'Add YouTube API key.': add_api_key,
         'How to add YouTube API key.': how_to_add_api_key,
         'Found channels.': found_channels,
         'Channel data.': channel_data,
         'Videos.': channel_videos,
         'Back to Channel data.': back_to_channel_data
         }
