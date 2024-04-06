import curses
import time
import random

def draw_log_panel(window, height, width):
    log_win = window.subwin(height, width, 0, 0)
    log_win.box()
    log_win.addstr(0, 2, ' Log Entries ', curses.A_REVERSE)
    for i in range(1, height - 1):
        log_win.addstr(i, 1, f'Log entry {i}')
    log_win.refresh()

def draw_bar_chart(window, height, width, start_row, start_col):
    chart_win = window.subwin(height, width, start_row, start_col)
    chart_win.box()
    chart_win.addstr(0, 2, ' Bar Chart ', curses.A_REVERSE)
    for i in range(1, height - 1):
        bar_width = random.randint(1, width - 2)
        chart_win.addstr(i, 1, '#' * bar_width)
    chart_win.refresh()

def draw_number_panel(window, height, width, start_row, start_col):
    num_win = window.subwin(height, width, start_row, start_col)
    num_win.box()
    num_win.addstr(0, 2, ' Numbers ', curses.A_REVERSE)
    num_win.addstr(1, 1, f'Number: {random.randint(0, 100)}')
    num_win.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()  # Clear the terminal
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    while True:
        draw_log_panel(stdscr, height // 2, width // 2)
        draw_bar_chart(stdscr, height // 2, width // 2, 0, width // 2)
        draw_number_panel(stdscr, height // 2, width // 2, height // 2, 0)
        stdscr.refresh()
        time.sleep(1)  # Update every second

if __name__ == '__main__':
    curses.wrapper(main)

