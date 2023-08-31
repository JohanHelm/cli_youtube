from collections import namedtuple
from api_key import KEY

MenuItem = namedtuple('MenuItem', ('message', 'choices', 'demand_user_input'), defaults=(False, ))

main_menu = MenuItem('Привет, это консольный клиент для видеохостинга YOUTUBE',
                     ('Найти видео.', 'Найти канал.', 'Открыть свои избранные каналы.', 'YOUTUBE API KEY', 'Выход'))

find_video = MenuItem('Введите название видео', ('Назад в Главное меню.', 'Выход'), True)

find_channel = MenuItem('Введите название канала', ('Назад в Главное меню.', 'Выход'), True)

my_favorite = MenuItem('Мои избранные каналы', ('Назад в Главное меню.', 'Выход'))

youtube_api_key = MenuItem('Для работы клиенту необходим ключ YouTube API',
                           ('Добавить ключ.', 'Как добавить ключ.', 'Назад в Главное меню.', 'Выход'))

add_api_key = MenuItem(f'Скопируйте ваш youtube api ключ. Перед вставкой ключа нажмите enter на клавиатуре. '
                       f'Вставьте ключ нажав комбинацию клавиш ctr+C+V и затем enter. '
                       f'Обязательно проверьте что ключ совпадает.'
                       f'Если не хотите менять ваш ключ оставьте поле ввода пустым и нажмите enter. '
                       f'Ваш youtube api ключ: {KEY}', ('Назад в YOUTUBE API KEY', 'Выход'), True)

how_to_get_api_key_msg = f'1. Авторизуйтесь в вашем аккаунте google.\n' \
                         '2. Перейдите в Google Cloud Console: https://console.developers.google.com/\n' \
                         '3. Создайте проект, если его еще нет.\n' \
                         '4. В разделе "API и сервисы" выберите "Учетные данные".\n' \
                         '5. Нажмите "Создать учетные данные" и выберите "ID клиента OAuth".\n' \
                         '6. Выберите тип приложения "Другое" или "Веб-приложение".\n' \
                         '7. После создания клиентского ID, скачайте JSON-файл с учетными данными,\n' \
                         'который будет содержать поля api_key client_id и client_secret.\n' \
                         'Для работы данного youtube клиента вам потребуется api_key'

how_to_add_api_key = MenuItem(how_to_get_api_key_msg, ('Назад в YOUTUBE API KEY', 'Выход'))

found_channes = MenuItem('Чтобы добавить канал в избранное выберите его и нажмите enter', ('Назад в Главное меню.', 'Выход'))

menu = {'Главное меню.': main_menu,
        'Найти видео.': find_video,
        'Найти канал.': find_channel,
        'Открыть свои избранные каналы.': my_favorite,
        'YOUTUBE API KEY': youtube_api_key,
        'Добавить ключ.': add_api_key,
        'Как добавить ключ.': how_to_add_api_key,
        'Каналы найдены.': found_channes}
