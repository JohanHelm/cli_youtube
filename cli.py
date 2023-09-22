from menus import menus
from settings import settings


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


def chunk_menu_options(items: tuple | list, lenght: int) -> tuple:
    item_height = 0
    items = list(items)
    for i, option in enumerate(items):
        items[i] = chunk_menu_text(option, lenght)[0]
        if len(items[i].split('\n')) > item_height:
            item_height = len(items[i].split('\n'))
    interval = item_height + settings.SUBINTERVAL  # интервал между опциями меню
    menu_options_height = len(items) * interval - settings.SUBINTERVAL  # Общая высота вариантов менюшки
    return tuple(items), menu_options_height, interval


def give_menu(level: str, string_lenght: int) -> tuple:
    if isinstance(menus[level].message, str):
        message = menus[level].message
    else:
        message = menus[level].message()
    if isinstance(menus[level].choices, tuple):
        options = menus[level].choices
    else:
        options = menus[level].choices()
    menu_items, menu_options_height, interval = chunk_menu_options(options, string_lenght)
    menu_text, menu_text_height = chunk_menu_text(message, string_lenght)

    return menu_text, menu_text_height, menu_items, menu_options_height, interval, menus[level].demand_user_input
