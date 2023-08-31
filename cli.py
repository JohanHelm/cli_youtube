from menus import menu


def chunk_menu_text(text: str, lenght: int) -> tuple:
    result = []
    temp_list = []
    for word in text.split():
        print(word)
        temp_list.append(word)
        if len(' '.join(temp_list)) >= lenght:
            result.append(f'{" ".join(temp_list[:-1])}\n')
            temp_list = [temp_list[-1]]
    result.append(' '.join(temp_list))
    return ' '.join(result), len(result)


def chunk_menu_options(items: tuple, lenght: int) -> tuple:
    item_height = 0
    items = list(items)
    for i, option in enumerate(items):
        items[i] = chunk_menu_text(option, lenght)[0]
        if len(items[i].split('\n')) > item_height:
            item_height = len(items[i].split('\n'))
    interval = item_height + 1  # интервал между опциями меню
    menu_options_height = len(items) * interval - 1  # Общая высота вариантов менюшки
    return tuple(items), menu_options_height, interval


def give_menu(level: str, string_lenght: int, search_result) -> tuple:
    menu_text, menu_text_height = chunk_menu_text(menu[level].message, string_lenght)
    if level in ('Каналы найдены.', 'Видео найдены.'):

        menu_items, menu_options_height, interval = chunk_menu_options(search_result + list(menu[level].choices), string_lenght)
    else:
        menu_items, menu_options_height, interval = chunk_menu_options(menu[level].choices, string_lenght)
    return menu_text, menu_text_height, menu_items, menu_options_height, interval, menu[level].demand_user_input

# chunk_menu_text(menu['Как добавить ключ'].message, 132 - 10)
# print(chunk_menu_text(menu['Как добавить ключ'].message, 132 - 10))
