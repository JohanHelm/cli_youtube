from menus import menu
from database import db


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
    subinterval = 0
    item_height = 0
    items = list(items)
    for i, option in enumerate(items):
        items[i] = chunk_menu_text(option, lenght)[0]
        if len(items[i].split('\n')) > item_height:
            item_height = len(items[i].split('\n'))
    interval = item_height + subinterval  # интервал между опциями меню
    menu_options_height = len(items) * interval - subinterval  # Общая высота вариантов менюшки
    return tuple(items), menu_options_height, interval


def get_pagination(page, pages, level, channels_data):
    pagination = []
    if page < pages:
        pagination.append('Вперёд')
    if page > 1:
        pagination.append('Назад')

    channels = [' '.join(i[1:]) for i in channels_data]
    channels.extend(pagination)
    channels.extend(list(menu[level].choices))
    return channels


def give_menu(level: str, string_lenght: int, page: int, show_results: int, item_to_show: int) -> tuple:
    message = menu[level].message
    results_amount = 0
    if level == 'Каналы найдены.':
        found_channels_data, pages = db.show_temp_channels(page, show_results)
        results_amount = len(found_channels_data)
        menu_items, menu_options_height, interval = chunk_menu_options(get_pagination(page, pages, level, found_channels_data[1:]), string_lenght)
    elif level == 'Мои избранные каналы.':
        my_channels_data, pages = db.show_my_channels(page, show_results)
        results_amount = len(my_channels_data)
        menu_items, menu_options_height, interval = chunk_menu_options(get_pagination(page, pages, level, my_channels_data), string_lenght)
    elif level == 'Данные канала.':
        channel_id, *chosen_channel_data = db.show_my_channels(page, show_results)[0][item_to_show]
        message = ' '.join(chosen_channel_data)
        menu_items, menu_options_height, interval = chunk_menu_options(menu[level].choices, string_lenght)
    else:
        menu_items, menu_options_height, interval = chunk_menu_options(menu[level].choices, string_lenght)
    menu_text, menu_text_height = chunk_menu_text(message, string_lenght)
    return menu_text, menu_text_height, menu_items, menu_options_height, interval, menu[level].demand_user_input, results_amount

# chunk_menu_text(menu['Как добавить ключ'].message, 132 - 10)
# print(chunk_menu_text(menu['Как добавить ключ'].message, 132 - 10))
# print(give_menu('Мои избранные каналы.', 130, 1, 5 ,0))
# print(give_menu('Каналы найдены.', 130, 1, 5 ,0))
# print(menu['Данные канала.'].choices)
