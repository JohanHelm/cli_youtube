from search_channels import channel_search

def input_hendler(menu_level, user_input):
    if menu_level == 'Добавить ключ.' and user_input:
        with open('api_key.py', 'w', encoding='utf-8') as file:
            file.write(f'KEY = "{user_input}"')
        return menu_level, None
    elif menu_level == 'Найти канал.' and user_input:
        return 'Каналы найдены.', channel_search.find_channel(user_input)
    else:
        return menu_level, None


