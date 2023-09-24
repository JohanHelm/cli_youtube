import curses

from cli import give_menu
from globals import gp
from menus import menus
from settings import settings
from user_input import input_handler


class CliMenuLoop:
    def create_menu(self, stdscr):
        # Disable cursor display
        curses.curs_set(0)
        # Get window size
        height, width = stdscr.getmaxyx()
        menu_height = height - 2
        menu_width = width - 2

        # Create new window for menu
        menu_win = curses.newwin(menu_height, menu_width, settings.MENU_Y, settings.MENU_X)
        menu_win.box()

        while True:
            menu_win.clear()
            # Call give_menu from cli
            menu_text, menu_text_height, menu_items, menu_options_height, interval, demand_user_input = give_menu(
                gp.MENU_LEVEL, menu_width - 10)

            vertical_shift_2 = menu_height - menu_options_height  # отступ сверху перед опциями

            # Place text in window
            menu_win.addstr(settings.VERTICAL_SHIFT_1, settings.HORIZONTAL_SHIFT_1, menu_text)

            # Place options in window
            for i, item in enumerate(menu_items):
                lines = item.split('\n')  # Split big text by strings
                for j, line in enumerate(lines):
                    if i == gp.SELECTED_ITEM:
                        menu_win.addstr(i * interval + j + vertical_shift_2, settings.HORIZONTAL_SHIFT_2, line,
                                        curses.A_REVERSE)
                    else:
                        menu_win.addstr(i * interval + j + vertical_shift_2, settings.HORIZONTAL_SHIFT_2, line)

            # Create service message
            menu_win.addstr(menu_height - menu_text_height - menu_options_height - 4 * interval, 2,
                            f"Status log: {gp.STATUS_MESSAGE}")

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
                else:
                    menus[gp.MENU_LEVEL].choice_handler(menu_items)

            if demand_user_input and not gp.USER_INPUT:
                curses.echo()  # Enable on-screen input display
                gp.USER_INPUT = stdscr.getstr(menu_text_height + 1, settings.HORIZONTAL_SHIFT_1 + 4, menu_width - 4)
                try:
                    gp.USER_INPUT = gp.USER_INPUT.decode("utf-8")
                except Exception as error:
                    print(error)
                else:
                    curses.noecho()  # Disable on-screen input display
                    gp.MENU_LEVEL = input_handler(gp.MENU_LEVEL, gp.USER_INPUT)

        curses.endwin()


create_menu_loop = CliMenuLoop()
# print(asizeof.asizeof(create_menu_loop))
