import curses

from cli import give_menu
from user_input import input_hendler
from database import db
from youtube import yt


def main(stdscr):
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

    # Выбранный пункт меню
    selected_item = 0
    menu_level = 'Главное меню.'  # Инициализируем переменную
    user_input = None
    search_results = None

    while True:
        menu_win.clear()
        # Вызов give_menu из cli, c с передачей уровня меню и длины строки Параметры менюшки: текст, опции
        menu_text, menu_text_height, menu_items, menu_options_height, interval, demand_user_input = give_menu(
            menu_level, menu_width - 10, search_results)

        vertical_shift_1 = 0  # отступ сверху перед текстом
        horizontal_shift_1 = 3  # отступ слева перед текстом
        # отступ сверху перед первым вариантом
        vertical_shift_2 = menu_height - menu_options_height  # отступ сверху перед опциями
        horizontal_shift_2 = 2  # отступ слева перед вариантами

        # Размещает текст
        menu_win.addstr(vertical_shift_1, horizontal_shift_1, menu_text)

        # Размещает опции
        for i, item in enumerate(menu_items):
            lines = item.split('\n')  # Разделяем многострочный текст на строки
            for j, line in enumerate(lines):
                if i == selected_item:
                    menu_win.addstr(i * interval + j + vertical_shift_2, horizontal_shift_2, line, curses.A_REVERSE)
                else:
                    menu_win.addstr(i * interval + j + vertical_shift_2, horizontal_shift_2, line)

        menu_win.addstr(menu_height - menu_text_height - menu_options_height - interval, 2,
                        f"Выбрано: {menu_level} {demand_user_input} {user_input}")

        menu_win.refresh()

        # Получаем нажатие клавиши
        key = stdscr.getch()

        if key == curses.KEY_UP and selected_item > 0:
            selected_item -= 1
        elif key == curses.KEY_DOWN and selected_item < len(menu_items) - 1:
            selected_item += 1
        elif key == ord('\n') or key == ord('\r'):
            if selected_item == len(menu_items) - 1:
                break  # Выход из меню
            elif menu_level == 'Каналы найдены.' and menu_items[selected_item].startswith('Канал: '):
                yt.add_fav_channel(selected_item)

            else:
                menu_level = menu_items[selected_item]
                if menu_level.startswith('Назад в '):
                    menu_level = menu_level.replace('Назад в ', '')
                    user_input = None

        if demand_user_input and not user_input:
            curses.echo()  # Включить отображение ввода на экране
            user_input = stdscr.getstr(menu_text_height + 1, horizontal_shift_1 + 4, menu_width - 4)
            user_input = user_input.decode("utf-8")
            curses.noecho()  # Выключить отображение ввода на экране
            menu_level, search_results = input_hendler(menu_level, user_input)

    # Завершение curses
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)
