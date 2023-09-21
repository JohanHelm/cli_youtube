import curses

from cli import give_menu
from globals import gp
from settings import settings
from user_input import input_hendler
from youtube import yt


class CliMenuLoop:
    def create_menu(self, stdscr):
        # Отключаем отображение курсора
        curses.curs_set(0)
        # Получаем размеры окна
        height, width = stdscr.getmaxyx()
        menu_height = height - 2
        menu_width = width - 2

        # Создаем новое окно для меню
        menu_win = curses.newwin(menu_height, menu_width, settings.MENU_Y, settings.MENU_X)
        menu_win.box()

        while True:
            menu_win.clear()
            # Вызов give_menu из cli, с передачей уровня меню и длины строки Параметры менюшки: текст, опции
            menu_text, menu_text_height, menu_items, menu_options_height, interval, demand_user_input, results_amount, \
            gp.CHANNEL_ID = give_menu(
                gp.MENU_LEVEL, menu_width - 10, gp.PAGE, gp.SHOW_RESULTS, gp.ITEM_TO_SHOW, gp.CHANNEL_ID)

            # отступ сверху перед первым вариантом
            vertical_shift_2 = menu_height - menu_options_height  # отступ сверху перед опциями

            # Place text in window
            menu_win.addstr(settings.VERTICAL_SHIFT_1, settings.HORIZONTAL_SHIFT_1, menu_text)

            # Place options in window
            for i, item in enumerate(menu_items):
                lines = item.split('\n')  # Разделяем многострочный текст на строки
                for j, line in enumerate(lines):
                    if i == gp.SELECTED_ITEM:
                        menu_win.addstr(i * interval + j + vertical_shift_2, settings.HORIZONTAL_SHIFT_2, line,
                                        curses.A_REVERSE)
                    else:
                        menu_win.addstr(i * interval + j + vertical_shift_2, settings.HORIZONTAL_SHIFT_2, line)

            menu_win.addstr(menu_height - menu_text_height - menu_options_height - interval, 2,
                            f"Status log: {menu_items}")

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
                    gp.PAGE += 1
                elif menu_items[gp.SELECTED_ITEM] == 'Back.':
                    gp.PAGE -= 1
                elif menu_items[gp.SELECTED_ITEM].startswith('Back to '):
                    gp.MENU_LEVEL = menu_items[gp.SELECTED_ITEM].replace('Back to ', '')
                    gp.USER_INPUT = None
                    gp.PAGE = 1
                elif menu_items[gp.SELECTED_ITEM] == 'Remove from favorites.':
                    gp.MENU_LEVEL = 'My favorites.'
                    yt.rm_channel(gp.CHANNEL_ID)
                elif gp.MENU_LEVEL == 'Found channels.' and gp.SELECTED_ITEM < results_amount:
                    yt.add_fav_channel(gp.PAGE, gp.SHOW_RESULTS, gp.SELECTED_ITEM)
                elif gp.MENU_LEVEL == 'My favorites.' and gp.SELECTED_ITEM < results_amount:
                    gp.MENU_LEVEL = 'Channel data.'
                    gp.ITEM_TO_SHOW = gp.SELECTED_ITEM
                elif gp.MENU_LEVEL == 'Videos.' and gp.SELECTED_ITEM < results_amount:
                    gp.ITEM_TO_SHOW = gp.SELECTED_ITEM
                    yt.playback_video(gp.PAGE, gp.SHOW_RESULTS, gp.SELECTED_ITEM, gp.CHANNEL_ID)
                else:
                    gp.MENU_LEVEL = menu_items[gp.SELECTED_ITEM]

            if demand_user_input and not gp.USER_INPUT:
                curses.echo()  # Включить отображение ввода на экране
                gp.USER_INPUT = stdscr.getstr(menu_text_height + 1, settings.HORIZONTAL_SHIFT_1 + 4, menu_width - 4)
                gp.USER_INPUT = gp.USER_INPUT.decode("utf-8")
                curses.noecho()  # Выключить отображение ввода на экране
                gp.MENU_LEVEL = input_hendler(gp.MENU_LEVEL, gp.USER_INPUT)

        curses.endwin()


create_menu_loop = CliMenuLoop()
