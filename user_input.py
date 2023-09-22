from youtube import yt


def input_handler(menu_level, user_input):
    if menu_level == 'Add api key.' and user_input:
        with open('api_key.py', 'w', encoding='utf-8') as file:
            file.write(f'KEY = "{user_input}"')
    elif menu_level == 'Find channel.' and user_input:
        yt.search_channel(user_input)
        menu_level = 'Found channels.'
    return menu_level

