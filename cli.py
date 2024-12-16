import curses
import argparse

from main import run

MODES = ["basic", "test"]
# Global variables
current_mode = "basic"
threshold = 0.85

def main(stdscr):
    global current_mode, threshold

    # Clear screen
    stdscr.clear()

    # Turn off cursor blinking
    curses.curs_set(0)

    # Options
    options = ["Start", "Options", "Threshold", "Exit"]
    current_option = 0

    while True:
        stdscr.clear()

        # Display the current mode and threshold at the top
        stdscr.addstr(0, 1, f"Current mode: {current_mode}")
        stdscr.addstr(1, 1, f"Threshold: {threshold}")

        # Display the options
        for idx, option in enumerate(options):
            if idx == current_option:
                stdscr.addstr(idx + 3, 1, option, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 3, 1, option)

        # Refresh the screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Move cursor based on key press
        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(options) - 1:
            current_option += 1
        elif key == ord('q'):
            break
        elif key == ord('\n'):
            if current_option == 0:  # Start option
                stdscr.clear()
                curses.endwin()
                res = run()
                stdscr = curses.initscr()
                stdscr.refresh()
                stdscr.addstr(0, 1, f"ROC: {round(res, 2)} | {"Success" if res >= threshold else "Failure"}")
                stdscr.getch()  # Wait for user to press a key
            elif current_option == 1:  # Options
                select_mode(stdscr)
            elif current_option == 2:  # Threshold
                set_threshold(stdscr)
            elif current_option == 3:  # Exit option
                break

def select_mode(stdscr):
    global current_mode

    modes = MODES
    current_mode_index = modes.index(current_mode)
    current_option = current_mode_index

    while True:
        stdscr.clear()
        stdscr.addstr(0, 1, "Select Mode:")

        # Display the modes
        for idx, mode in enumerate(modes):
            if idx == current_option:
                stdscr.addstr(idx + 1, 1, mode, curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 1, mode)

        # Refresh the screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Move cursor based on key press
        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(modes) - 1:
            current_option += 1
        elif key == ord('q'):
            break
        elif key == ord('\n'):
            current_mode = modes[current_option]
            break

def set_threshold(stdscr):
    global threshold

    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 1, "Set Threshold (0 to 1): ")
    stdscr.refresh()

    while True:
        try:
            input_str = stdscr.getstr(1, 1).decode('utf-8')
            new_threshold = float(input_str)
            if 0 <= new_threshold <= 1:
                threshold = new_threshold
                break
            else:
                stdscr.addstr(2, 1, "Invalid input. Please enter a value between 0 and 1.")
                stdscr.refresh()
        except ValueError:
            stdscr.addstr(2, 1, "Invalid input. Please enter a numeric value.")
            stdscr.refresh()

    curses.noecho()

def run_cli_mode(mode, threshold):
    global current_mode
    current_mode = mode
    res = run(current_mode)
    return "OK" if res >= threshold else "Fail"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="5G-Tactile-IDS CLI")
    parser.add_argument('-c', action='store_true', help="Run in command mode")
    parser.add_argument('-mode', type=str, choices=MODES, help="Set the mode")
    parser.add_argument('-t', type=float, help="Set the threshold value (0 to 1)")

    args = parser.parse_args()

    if args.c:
        if args.mode:
            r = run_cli_mode(args.mode, args.t)
            print(r)
        else:
            print("Please specify a mode with the -mode option")
    else:
        curses.wrapper(main)


# python cli.py -c -mode test -t 0.85   
