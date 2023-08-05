import curses
import time

TIME_DP = 1
ENTER_KEYS = {10, 13}


def print_char(scr, char, colour_profile):
    scr.attron(curses.color_pair(colour_profile))
    y, x = scr.getyx()
    scr.addstr(y, x, char)
    scr.attroff(curses.color_pair(colour_profile))


def wait_for_enter_pressed(scr):
    scr.nodelay(False)
    key = None
    while key not in ENTER_KEYS:
        key = scr.getch()
    return


def print_time(scr, row, start_time, reset_cursor_pos):
    scr.addstr(row, 0, f"Time taken: {round(time.time() - start_time, TIME_DP)}s")
    scr.move(4, reset_cursor_pos)
