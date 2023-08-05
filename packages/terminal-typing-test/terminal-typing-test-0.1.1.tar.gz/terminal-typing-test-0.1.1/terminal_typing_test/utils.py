import curses
import time

TIME_DP = 1
ENTER_KEYS = {10, 13}

def print_char(scr, char, colour_profile):
    scr.attron(curses.color_pair(colour_profile))
    y, x = scr.getyx()
    scr.addstr(y, x, char)
    move_back(scr)
    scr.attroff(curses.color_pair(colour_profile))

def move_forward(scr):
    y, x = scr.getyx()
    h, w = scr.getmaxyx()
    if x < w - 1:
        scr.move(y, x + 1)
    else:
        scr.move(y + 1, 0)

def move_back(scr):
    y, x = scr.getyx()
    h, w = scr.getmaxyx()
    if x > 0:
        scr.move(y, x - 1)
    else:
        scr.move(y - 1, w - 1)


def wait_for_enter_pressed(scr):
    scr.nodelay(False)
    key = None
    while key not in ENTER_KEYS:
        key = scr.getch()
    return


def print_time(scr, row, start_time):
    y, x = scr.getyx()
    scr.addstr(row, 0, f"Time taken: {round(time.time() - start_time, TIME_DP)}s")
    scr.move(y, x)
