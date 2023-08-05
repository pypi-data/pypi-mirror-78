from terminal_typing_test.utils import TIME_DP


class Monitor:
    def __init__(self, num_words_typed, start_time):
        self.num_words_typed = num_words_typed
        self.start_time = start_time
        self.end_time = None

    def print_results(self, scr, row):
        time_taken = self.end_time - self.start_time
        wpm = self.num_words_typed / time_taken * 60
        scr.addstr(row, 0, f"Time taken: {round(time_taken, TIME_DP)} seconds.")
        scr.addstr(row + 1, 0, f"Number of words typed: {self.num_words_typed}.")
        scr.addstr(row + 2, 0, f"Your WPM is {round(wpm, 1)}. Press Enter to quit.")
