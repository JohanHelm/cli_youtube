from enum import Enum

from menus import menus
from settings import settings


class MenuDispatcher:
    @staticmethod
    def chunk_menu_text(text: str, lenght: int) -> tuple:
        result = []
        temp_list = []
        for word in text.split():
            temp_list.append(word)
            if len(' '.join(temp_list)) >= lenght:
                result.append(f'{" ".join(temp_list[:-1])}\n')
                temp_list = [temp_list[-1]]
        result.append(' '.join(temp_list))
        return ' '.join(result), len(result)

    @staticmethod
    def chunk_menu_options(items: tuple | list, lenght: int) -> tuple:
        item_height = 0
        items = list(items)
        for i, option in enumerate(items):
            items[i] = MenuDispatcher.chunk_menu_text(option, lenght)[0]
            if len(items[i].split('\n')) > item_height:
                item_height = len(items[i].split('\n'))
        interval = item_height + settings.SUBINTERVAL  # интервал между опциями меню
        menu_options_height = len(items) * interval - settings.SUBINTERVAL  # Общая высота вариантов менюшки
        menu_items = Enum('Options', items, start=0)
        return menu_items, menu_options_height, interval

    @staticmethod
    def give_menu(level: str, string_lenght: int) -> tuple:
        message = menus[level].create_message()
        options = menus[level].create_choices()
        menu_items, menu_options_height, interval = MenuDispatcher.chunk_menu_options(options, string_lenght)
        menu_text, menu_text_height = MenuDispatcher.chunk_menu_text(message, string_lenght)

        return menu_text, menu_text_height, menu_items, menu_options_height, interval, menus[level].demand_user_input


md = MenuDispatcher()
