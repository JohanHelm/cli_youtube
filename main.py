import curses

from main_loop import CliMenuLoop

"""
This is a command-line interface YouTube client application.
It enables ad-free YouTube video viewing by bypassing Google ads and integrated advertising.

To use this application, you'll need a Google Application API key.

It utilizes the MPV media player for playing YouTube videos and shorts.
"""

if __name__ == "__main__":
    create_menu_loop = CliMenuLoop()
    curses.wrapper(create_menu_loop.create_menu)
