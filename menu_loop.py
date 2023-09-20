import curses

from cli import give_menu
from user_input import input_hendler
from youtube import yt
from globals import gp

class CliMenuLoop:
    def create_menu(self, stdscr):
        # Отключаем отображение курсора
        curses.curs_set(0)
        # Получаем размеры окна
        height, width = stdscr.getmaxyx()
        menu_height = height - 2
        menu_width = width - 2
        menu_y = 1
        menu_x = 5
        # Создаем новое окно для меню
        menu_win = curses.newwin(menu_height, menu_width, menu_y, menu_x)
        menu_win.box()

        # selected_item = 0
        # menu_level = 'Main menu.'
        user_input = None
        show_results = 5
        page = 1
        item_to_show = None
        channel_id = None
        playlist_id = None

        while True:
            menu_win.clear()
            # Вызов give_menu из cli, c с передачей уровня меню и длины строки Параметры менюшки: текст, опции
            menu_text, menu_text_height, menu_items, menu_options_height, interval, demand_user_input, results_amount, channel_id = \
                give_menu(gp.MENU_LEVEL, menu_width - 10, page, show_results, item_to_show, channel_id)

            vertical_shift_1 = 0  # отступ сверху перед текстом
            horizontal_shift_1 = 3  # отступ слева перед текстом
            # отступ сверху перед первым вариантом
            vertical_shift_2 = menu_height - menu_options_height  # отступ сверху перед опциями
            horizontal_shift_2 = 2  # отступ слева перед вариантами

            # Place text in window
            menu_win.addstr(vertical_shift_1, horizontal_shift_1, menu_text)

            # Place options in window
            for i, item in enumerate(menu_items):
                lines = item.split('\n')  # Разделяем многострочный текст на строки
                for j, line in enumerate(lines):
                    if i == gp.SELECTED_ITEM:
                        menu_win.addstr(i * interval + j + vertical_shift_2, horizontal_shift_2, line, curses.A_REVERSE)
                    else:
                        menu_win.addstr(i * interval + j + vertical_shift_2, horizontal_shift_2, line)

            menu_win.addstr(menu_height - menu_text_height - menu_options_height - interval, 2,
                            f"Status log: {gp.MENU_LEVEL} {demand_user_input} {gp.USER_INPUT} {menu_height} {menu_width} {item_to_show}")

            menu_win.refresh()

            # Get user pressed key
            key = stdscr.getch()

            if key == curses.KEY_UP and gp.SELECTED_ITEM > 0:
                gp.SELECTED_ITEM -= 1
            elif key == curses.KEY_DOWN and gp.SELECTED_ITEM < len(menu_items) - 1:
                gp.SELECTED_ITEM += 1
            elif key == ord('\n') or key == ord('\r'):
                if gp.SELECTED_ITEM == len(menu_items) - 1:
                    break  # Quit
                elif menu_items[gp.SELECTED_ITEM] == 'Forward.':
                    page += 1
                elif menu_items[gp.SELECTED_ITEM] == 'Back.':
                    page -= 1
                elif menu_items[gp.SELECTED_ITEM].startswith('Back to '):
                    gp.MENU_LEVEL = menu_items[gp.SELECTED_ITEM].replace('Back to ', '')
                    gp.USER_INPUT = None
                elif menu_items[gp.SELECTED_ITEM] == 'Remove from favorites.':
                    gp.MENU_LEVEL = 'My favorites.'
                    yt.rm_channel(channel_id)
                elif gp.MENU_LEVEL == 'Found channels.' and gp.SELECTED_ITEM < results_amount:
                    yt.add_fav_channel(page, show_results, gp.SELECTED_ITEM)
                elif gp.MENU_LEVEL == 'My favorites.' and gp.SELECTED_ITEM < results_amount:
                    gp.MENU_LEVEL = 'Channel data.'
                    item_to_show = gp.SELECTED_ITEM
                elif gp.MENU_LEVEL == 'Videos.' and gp.SELECTED_ITEM < results_amount:
                    item_to_show = gp.SELECTED_ITEM
                    yt.playback_video(page, show_results, gp.SELECTED_ITEM, channel_id)
                else:
                    gp.MENU_LEVEL = menu_items[gp.SELECTED_ITEM]

            if demand_user_input and not gp.USER_INPUT:
                curses.echo()  # Включить отображение ввода на экране
                gp.USER_INPUT = stdscr.getstr(menu_text_height + 1, horizontal_shift_1 + 4, menu_width - 4)
                gp.USER_INPUT = gp.USER_INPUT.decode("utf-8")
                curses.noecho()  # Выключить отображение ввода на экране
                gp.MENU_LEVEL = input_hendler(gp.MENU_LEVEL, gp.USER_INPUT)

        curses.endwin()


create_menu_loop = CliMenuLoop()
