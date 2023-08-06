import curses
import os
import random
import sys
import time

from terminal_typing_test.monitor import Monitor
from terminal_typing_test.utils import move_forward, move_back, print_time, print_char, wait_for_enter_pressed

ESCAPE = 27
BACKSPACE_KEYS = {8, 127, 263}

CORRECT_COLOUR = 1
ERROR_COLOUR = 2
RESET_COLOUR = 3

text_directory = os.path.join(os.path.dirname(__file__), "text/short/")
file = random.choice(os.listdir(text_directory))
with open(text_directory + file) as f:
    TEST_STRING = f.read()
    TEST_STRING_LENGTH = len(TEST_STRING)


def main(stdscr):
    curses.use_default_colors()
    curses.init_pair(CORRECT_COLOUR, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(ERROR_COLOUR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(RESET_COLOUR, -1, -1)
    stdscr.nodelay(True)

    monitor = Monitor(1, time.time())
    curr_char_idx = 0

    stdscr.addstr(0, 0, "Welcome to Typing Test! Press Ctrl-C to quit.")
    stdscr.addstr(4, 0, "Type the following:")
    stdscr.addstr(5, 0, TEST_STRING)
    stdscr.move(5, 0)

    while True:
        try:
            key = stdscr.getch()
            print_time(stdscr, 2, monitor.start_time)
        except KeyboardInterrupt:
            sys.exit()

        if key == curses.ERR:
            pass
        elif key == ESCAPE:
            break
        elif key in BACKSPACE_KEYS:
            if curr_char_idx > 0:
                print_char(stdscr, TEST_STRING[curr_char_idx], RESET_COLOUR)
                curr_char_idx -= 1
                move_back(stdscr)
        else:
            if curr_char_idx < TEST_STRING_LENGTH - 1:
                if TEST_STRING[curr_char_idx] == " ":
                    monitor.num_words_typed += 1
                colour_profile = CORRECT_COLOUR if key == ord(TEST_STRING[curr_char_idx]) else ERROR_COLOUR
                print_char(stdscr, TEST_STRING[curr_char_idx], colour_profile)
                curr_char_idx += 1
                move_forward(stdscr)
            else:
                monitor.end_time = time.time()
                stdscr.clear()
                monitor.print_results(stdscr, row=0)
                wait_for_enter_pressed(stdscr)
                break


def run():
    curses.wrapper(main)
