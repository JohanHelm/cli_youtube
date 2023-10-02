import youtube as yt
from database import db
from globals import gp
from youtube_api.api_key import KEY


class MenuGenerator:
    __slots__ = ('demand_user_input',)

    def __init__(self, demand_user_input=False):
        self.demand_user_input = demand_user_input

    @staticmethod
    def pagination(pages: int, responce_data: tuple, page: int) -> tuple:
        results_amount = len(responce_data)
        result = [' '.join(i[1:]) for i in responce_data]
        if page < pages:
            result.append('Forward.')
        if page > 1:
            result.append('Back.')
        return result, results_amount

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
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

    def choice_handler(self, menu_items, selected_item, menu_level, page, user_input, status_message):
        """
        Takes user choice and executes further actions
        :return: None
        """
        if menu_items(selected_item).name == 'Forward.':
            page += 1
        elif menu_items(selected_item).name == 'Back.':
            page -= 1
        elif menu_items(selected_item).name.startswith('Back to '):
            menu_level = menu_items(selected_item).name.replace('Back to ', '')
            user_input = None
            page = 1
            status_message = ''
        # elif gp.SELECTED_ITEM == len(menu_items):
        #     quit(0)
        else:
            menu_level = menu_items(selected_item).name

        return menu_level, page, user_input, status_message


class MainMenu(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
        message = 'Hi, this is YOUTUBE command line client.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Find channel.', 'My favorites.', 'YOUTUBE API KEY.', 'Exit.')
        return options, 0


class FindChannel(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__(True)

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
        message = 'Type channel title.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Back to Main menu.', 'Exit.')
        return options, 0

    def choice_handler(self, menu_items, selected_item, menu_level, page, user_input, status_message):
        if user_input:
            yt.search_channel(user_input)
            menu_level = 'Found channels.'
            user_input = ''
        else:
            menu_level, page, user_input, status_message = MenuGenerator.choice_handler(self, menu_items, selected_item,
                                                                                        menu_level, page, user_input,
                                                                                        status_message)
        return menu_level, page, user_input, status_message


class MyFavotrite(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
        message = 'My favorite channels.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        my_channels_data, pages = db.show_my_channels(page, show_results)
        options, results_amount = MenuGenerator.pagination(pages, my_channels_data, page)
        options.extend(['Back to Main menu.', 'Exit.'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item, menu_level, page, user_input, status_message):
        if gp.SELECTED_ITEM < gp.RESULTS_AMOUNT:
            gp.MENU_LEVEL = 'Channel data.'
            gp.ITEM_TO_SHOW = gp.SELECTED_ITEM
        else:
            MenuGenerator.choice_handler(self, menu_items)


class YotubeApiKey(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
        message = 'This application needs YouTube API key.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Add YouTube API key.', 'How to add YouTube API key.', 'Back to Main menu.', 'Exit.')
        return options, 0


class AddApiKey(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__(True)

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
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

    def choice_handler(self, menu_items):
        if gp.USER_INPUT:
            with open('api_key.py', 'w', encoding='utf-8') as file:
                file.write(f'KEY = "{gp.USER_INPUT}"')
            gp.USER_INPUT = ''
        else:
            MenuGenerator.choice_handler(self, menu_items)


class HowToAddApiKey(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, channel_id: str, item_to_show: int) -> tuple:
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

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
        message = 'Choose channel and press enter to add it in favorites.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> list:
        found_channels_data, pages = db.show_temp_channels(page, show_results)
        options, results_amount = MenuGenerator.pagination(pages, found_channels_data, page)
        options.extend(['Back to Main menu.', 'Exit.'])
        return options, results_amount

    def choice_handler(self, menu_items):
        if gp.SELECTED_ITEM < gp.RESULTS_AMOUNT:
            yt.add_fav_channel(gp.PAGE, gp.SHOW_RESULTS, gp.SELECTED_ITEM)
        else:
            MenuGenerator.choice_handler(self, menu_items)


class ChannelData(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
        channel_id, *chosen_channel_data = db.show_my_channels(page, show_results)[0][item_to_show]
        return channel_id, ' '.join(chosen_channel_data)

    def create_choices(self, page: int, show_results: int, channel_id: str) -> tuple:
        options = ('Remove from favorites.', 'Update the list of video.', 'Videos.', 'Back to My favorites.', 'Exit.')
        return options, 0

    def choice_handler(self, menu_items):
        # if menu_items(gp.SELECTED_ITEM).name == 'Remove from favorites.':
        if gp.SELECTED_ITEM == 0:
            gp.MENU_LEVEL = 'My favorites.'
            yt.rm_channel(gp.CHANNEL_ID)
        # elif menu_items(gp.SELECTED_ITEM).name == 'Update the list of video.':
        elif gp.SELECTED_ITEM == 1:
            yt.update_channel_videos(gp.CHANNEL_ID)
        else:
            MenuGenerator.choice_handler(self, menu_items)


class ChannelVideos(MenuGenerator):
    __slots__ = ('demand_user_input',)

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int) -> tuple:
        message = 'Choose video and press enter for playback.'
        return '', message

    def create_choices(self, page: int, show_results: int, channel_id: str) -> list:
        channel_videos_data, pages = db.show_channel_videos(page, show_results, channel_id)
        options, results_amount = MenuGenerator.pagination(pages, channel_videos_data, page)
        options.extend(['Back to Channel data.', 'Exit.'])
        return options, results_amount

    def choice_handler(self, menu_items):
        if gp.SELECTED_ITEM < gp.RESULTS_AMOUNT:
            gp.ITEM_TO_SHOW = gp.SELECTED_ITEM
            yt.playback_video(gp.PAGE, gp.SHOW_RESULTS, gp.SELECTED_ITEM, gp.CHANNEL_ID)
        else:
            MenuGenerator.choice_handler(self, menu_items)


class Goodbye():
    """
    Just close the application
    """

    def create_message(self, page: int, show_results: int, item_to_show: int):
        quit(0)


main_menu = MainMenu()
find_channel = FindChannel()
my_favorite = MyFavotrite()
youtube_api_key = YotubeApiKey()
add_api_key = AddApiKey()
how_to_add_api_key = HowToAddApiKey()
found_channels = FoundChannels()
channel_data = ChannelData()
channel_videos = ChannelVideos()
goodbye = Goodbye()

menus = {'Main menu.': main_menu,
         'Find channel.': find_channel,
         'My favorites.': my_favorite,
         'YOUTUBE API KEY.': youtube_api_key,
         'Add YouTube API key.': add_api_key,
         'How to add YouTube API key.': how_to_add_api_key,
         'Found channels.': found_channels,
         'Channel data.': channel_data,
         'Videos.': channel_videos,
         'Exit.': goodbye
         }
