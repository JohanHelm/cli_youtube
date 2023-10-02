import curses

from menu.menu_disptcher import give_menu
from globals import gp
from menu.menus import menus
from settings import settings
from exceptions import exceptions_handler


class CliMenuLoop:
    __slots__ = ('selected_item', 'menu_level', 'user_input', 'show_results', 'page', 'item_to_show', 'channel_id',
                 'status_message', 'results_amount', 'version')

    def __init__(self):
        self.selected_item: int = 0
        self.menu_level: str = 'Main menu.'
        self.user_input: str = ''
        self.show_results: int = 5
        self.page: int = 1
        self.item_to_show: int = 0
        self.channel_id: str = ''
        self.status_message: str = ''
        self.results_amount: int = 0
        self.version: float = 1.0

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
                self.menu_level, menu_width - 10)

            vertical_shift_2 = menu_height - menu_options_height

            # Place text in window
            menu_win.addstr(settings.VERTICAL_SHIFT_1, settings.HORIZONTAL_SHIFT_1, menu_text)

            # Place options in window
            for item in menu_items:
                lines = item.name.split('\n')  # Split big text by strings
                for j, line in enumerate(lines):
                    if item.value == self.selected_item:
                        menu_win.addstr(item.value * interval + j + vertical_shift_2, settings.HORIZONTAL_SHIFT_2, line,
                                        curses.A_REVERSE)
                    else:
                        menu_win.addstr(item.value * interval + j + vertical_shift_2, settings.HORIZONTAL_SHIFT_2, line)
            self.status_message = self.menu_level
            if self.status_message:  # Create service message
                menu_win.addstr(menu_height - menu_text_height - menu_options_height - 2 * interval, 2,
                                f"Status log: {self.status_message}")

            menu_win.refresh()

            # Get user pressed key
            key = stdscr.getch()

            if key == curses.KEY_UP and self.selected_item > 0:
                self.selected_item -= 1
            elif key == curses.KEY_DOWN and self.selected_item < len(menu_items) - 1:
                self.selected_item += 1
            elif key == ord('\n') or key == ord('\r'):
                menus[self.menu_level].choice_handler(menu_items)

            if demand_user_input and not self.user_input:
                curses.echo()  # Enable on-screen input display
                self.user_input = stdscr.getstr(menu_text_height + 1, settings.HORIZONTAL_SHIFT_1 + 4, menu_width - 4)
                try:
                    self.user_input = self.user_input.decode("utf-8")
                except Exception as error:
                    exceptions_handler(error)
                else:
                    curses.noecho()  # Disable on-screen input display
                    menus[self.menu_level].choice_handler(menu_items)

        # curses.endwin()


create_menu_loop = CliMenuLoop()