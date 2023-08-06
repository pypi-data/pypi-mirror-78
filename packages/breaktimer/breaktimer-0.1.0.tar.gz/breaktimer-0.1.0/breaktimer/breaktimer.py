import time as t
import click
import curses
from curses import wrapper
from pyfiglet import Figlet


def format_time(minutes, seconds):
    minute_str = f'{minutes} minutes' if minutes > 1 else (
        f'{minutes} minute' if minutes > 0 else "")
    second_str = f'{seconds} seconds' if seconds > 1 else (
        f'{seconds} second' if seconds > 0 else "")
    return f'{minute_str} {second_str}'


@click.command()
@click.option("--minutes", "-m", default=None)
@click.option("--banner", "-b", default="Break Timer")
def breaktimer(minutes, banner):
    stdscr = curses.initscr()
    num_rows, num_cols = stdscr.getmaxyx()

    curses.curs_set(0)  # disable cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    custom_fig = Figlet(font='digital')
    ascii_banner = custom_fig.renderText(banner)

    stdscr.addstr(0, 0, ascii_banner)
    # this will enable to utilize specified functions within time library such as sleep()
    # Asking user the duration for which the user wants to delay the process
    break_duration = int(minutes)
    break_duration *= 60  # convert to seconds

    middle_row = int(num_rows/2)
    middle_column = int(num_cols/2)

    # Let's use a ranged loop to create the counter
    for tick in range(break_duration, 0, -1):
        # we also need the loop to wait for 1 second between each iteration
        minutes_left = int(tick/60)
        seconds_left = tick % 60
        stdscr.clrtoeol()
        time_left = format_time(minutes_left, seconds_left).strip()
        half_length_message = int(len(time_left) / 2)
        x_position = middle_column - half_length_message
        stdscr.addstr(
            middle_row, x_position, time_left, curses.color_pair(1) | curses.A_BOLD)
        stdscr.refresh()
        t.sleep(1)

    end_of_time_message = "<< Break is over >>"
    stdscr.addstr(middle_row, middle_column -
                  int(len(end_of_time_message)/2), end_of_time_message, curses.A_REVERSE)
    c = stdscr.getch()

    curses.curs_set(1)
    curses.endwin()


if __name__ == "__main__":
    breaktimer()
