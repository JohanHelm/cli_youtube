from os import chdir, getcwd
from os.path import expanduser
from subprocess import PIPE, Popen

from database import Database
from youtube import YoutubeManager
from youtube_api.api_key import KEY


class MenuGenerator:
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self, demand_user_input=False):
        self.demand_user_input = demand_user_input
        self.db = Database(f'{expanduser("~")}/.local/share/cli_youtube/my_favorites.db')
        self.yt = YoutubeManager()

    @staticmethod
    def pagination(pages: int, responce_data: tuple, current_page: int) -> tuple[list, int]:
        results_amount = len(responce_data)
        result = [' '.join(i[1:]) for i in responce_data]
        if current_page < pages:
            result.append('Forward')
        if current_page > 1:
            result.append('Back')
        return result, results_amount

    @staticmethod
    def check_for_updates():
        current_directory = getcwd()
        chdir(f'{expanduser("~")}/.local/share/cli_youtube/')
        cmd = f'git pull origin cli '
        update_request = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
        update_result = update_request.communicate()[0]
        if 'Already up to date.\n' in update_result:
            chdir(current_directory)
        else:
            quit(0)

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[str, str]:
        """
        Creates menu message
        Get unit_id
        :return: unit_id, message
        """

    def create_choices(self, page: list, show_results: int, unit_id: str) -> tuple:
        """
        Create menu options
        save options amount in results_amount
        :return: options, results_amount
        """

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        """
        Takes user choice and executes further actions
        :return: tuple[str, list, str, str, int]
        """

        if selected_item == len(menu_items) - 1:  # 'Exit.'
            quit(0)
        elif menu_items(selected_item).name.startswith('Back_to_'):
            menu_level = menu_items(selected_item).name.replace('Back_to_', '')
            status_message = ''
        else:
            menu_level = menu_items(selected_item).name

        return menu_level, page, user_input, status_message, item_to_show


class MainMenu(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        message = 'Hi, this is YOUTUBE command line client.'
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple:
        options = ('Find_channel', 'My_favorites', 'YOUTUBE_API_KEY', 'Check_for_updates', 'Exit')
        return options, 0

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if selected_item == len(menu_items) - 2:  # 'Check_for_updates'
            MenuGenerator.check_for_updates()
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, item_to_show


class FindChannel(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__(True)

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[str, str]:
        message = 'Type channel title.'
        return '', message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple:
        options = ('Back_to_Main_menu', 'Exit')
        return options, 0

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if user_input:
            self.yt.search_channel(user_input)
            menu_level = 'Found_channels'
            user_input = ''
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, 0


class MyFavotrite(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: int, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        message = 'My favorite channels.'
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple[list, int]:
        my_channels_data, pages = self.db.show_my_channels(page[0], show_results)
        options, results_amount = MenuGenerator.pagination(pages, my_channels_data, page[0])
        options.extend(['Back_to_Main_menu', 'Exit'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if selected_item < results_amount:
            menu_level = 'Channel_data'
            item_to_show = selected_item
        elif menu_items(selected_item).name == 'Forward':
            page[0] += 1
        elif menu_items(selected_item).name == 'Back':
            page[0] -= 1
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, item_to_show


class YotubeApiKey(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        message = 'This application needs YouTube API key.'
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple:
        options = ('Add_YouTube_API_key', 'How_to_add_YouTube_API_key', 'Back_to_Main_menu', 'Exit')
        return options, 0


class AddApiKey(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__(True)

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        message = f'1. Copy your YouTube API key.\n' \
                  f'2. Press Enter before pasting the key.\n' \
                  f'3. Paste the key using Ctrl+C+V, then press Enter.\n' \
                  f'4. Ensure that the key matches.\n' \
                  f"5. If you don't want to change your key, leave the input field empty and press Enter.\n" \
                  f'Your youtube api key: {KEY}'
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple:
        options = ('Back_to_YOUTUBE_API_KEY', 'Exit')
        return options, 0

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if user_input:
            with open('api_key.py', 'w', encoding='utf-8') as file:
                file.write(f'KEY = "{user_input}"')
            user_input = ''
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, 0


class HowToAddApiKey(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
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
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple:
        options = ('Back_to_YOUTUBE_API_KEY', 'Exit')
        return options, 0


class FoundChannels(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        message = 'Choose channel and press enter to add it in favorites.'
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple[list, int]:
        found_channels_data, pages = self.db.show_temp_channels(page[0], show_results)
        options, results_amount = MenuGenerator.pagination(pages, found_channels_data, page[0])
        options.extend(['Back_to_Main_menu', 'Exit'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if selected_item < results_amount:
            self.yt.add_fav_channel(page[0], show_results, selected_item)
        elif menu_items(selected_item).name == 'Forward':
            page[0] += 1
        elif menu_items(selected_item).name == 'Back':
            page[0] -= 1
        else:
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, item_to_show


class ChannelData(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        unit_id[0], *chosen_channel_data = self.db.show_my_channels(page[0], show_results)[0][item_to_show]
        return unit_id, ' '.join(chosen_channel_data)

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple:
        options = (
            'Remove_from_favorites', 'Update_the_list_of_video', 'Playlists', 'Videos', 'Back_to_My_favorites', 'Exit')
        return options, 0

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if selected_item == 0:
            menu_level = 'My_favorites'
            self.yt.rm_channel(unit_id[0])
        elif selected_item == 1:
            self.yt.update_channel_data(unit_id[0])
        else:
            page[1] = 1
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, item_to_show


class ChannelVideos(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        message = 'Choose video and press enter for playback.'
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: str) -> tuple[list, int]:
        channel_videos_data, pages = self.db.show_channel_videos(page[1], show_results, unit_id[0])
        options, results_amount = MenuGenerator.pagination(pages, channel_videos_data, page[1])
        options.extend(['Back_to_Channel_data', 'Exit'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if selected_item < results_amount:
            item_to_show = selected_item
            self.yt.playback_channel_video(page[1], show_results, selected_item, unit_id[0])
        elif menu_items(selected_item).name == 'Forward':
            page[1] += 1
        elif menu_items(selected_item).name == 'Back':
            page[1] -= 1
        else:
            page[1] = 1
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, item_to_show


class ChannelPlaylists(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        message = 'Choose playlist and press enter to see summary.'
        return unit_id, message

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple[list, int]:
        channel_playlists_data, pages = self.db.show_channel_playlists(page[2], show_results, unit_id[0])
        options, results_amount = MenuGenerator.pagination(pages, channel_playlists_data, page[2])
        options.extend(['Back_to_Channel_data', 'Exit'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if selected_item < results_amount:
            item_to_show = selected_item
            menu_level = 'Playlist_data'
        elif menu_items(selected_item).name == 'Forward':
            page[2] += 1
        elif menu_items(selected_item).name == 'Back':
            page[2] -= 1
        else:
            page[2] = 1
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, item_to_show


class PlaylistData(MenuGenerator):
    __slots__ = ('demand_user_input', 'db', 'yt')

    def __init__(self):
        super().__init__()

    def create_message(self, page: list, show_results: int, item_to_show: int, unit_id: list) -> tuple[list, str]:
        # page = [1, 1, 1]  # [channels, videos, playlists]
        # unit_id = ['','','']  # [channel_id, video_id, playlist_ id]
        unit_id[2], *chosen_playlist_data = self.db.show_channel_playlists(page[2], show_results, unit_id[0])[0][
            item_to_show]
        return unit_id, ' '.join(chosen_playlist_data)

    def create_choices(self, page: list, show_results: int, unit_id: list) -> tuple[list, int]:
        chosen_playlist_data, pages = self.db.show_playlist_videos(page[1], show_results, unit_id[2])
        options, results_amount = MenuGenerator.pagination(pages, chosen_playlist_data, page[1])
        options.extend(['Back_to_Playlists', 'Exit'])
        return options, results_amount

    def choice_handler(self, menu_items, selected_item: int, menu_level: str, page: list, user_input: str,
                       status_message: str, results_amount: int, unit_id: list, item_to_show: int,
                       show_results: int) -> tuple[str, list, str, str, int]:
        if selected_item < results_amount:
            item_to_show = selected_item
            self.yt.playback_playlist_video(page[1], show_results, selected_item, unit_id[2])
        elif menu_items(selected_item).name == 'Forward':
            page[1] += 1
        elif menu_items(selected_item).name == 'Back':
            page[1] -= 1
        else:
            page[1] = 1
            menu_level, page, user_input, status_message, item_to_show = \
                MenuGenerator.choice_handler(self, menu_items, selected_item, menu_level, page, user_input,
                                             status_message, results_amount, unit_id, item_to_show, show_results)
        return menu_level, page, user_input, status_message, item_to_show


class Menus:
    def __init__(self):
        self.Main_menu = MainMenu()
        self.Find_channel = FindChannel()
        self.My_favorites = MyFavotrite()
        self.YOUTUBE_API_KEY = YotubeApiKey()
        self.Add_YouTube_API_key = AddApiKey()
        self.How_to_add_YouTube_API_key = HowToAddApiKey()
        self.Found_channels = FoundChannels()
        self.Channel_data = ChannelData()
        self.Videos = ChannelVideos()
        self.Playlists = ChannelPlaylists()
        self.Playlist_data = PlaylistData()
