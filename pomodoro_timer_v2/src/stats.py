import curses
from datetime import datetime, timedelta, date
from src.helper import print_debug
import csv
from src.data_manager import DataManager

days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]

CLR_GRADIENT_WHITE_TO_BLACK = [
    "\033[38;5;255m",  # Bright white
    "\033[38;5;254m",
    "\033[38;5;253m",
    "\033[38;5;252m",
    "\033[38;5;251m",
    "\033[38;5;250m",
    "\033[38;5;249m",
    "\033[38;5;248m",
    "\033[38;5;247m",
    "\033[38;5;246m",
    "\033[38;5;245m",
    "\033[38;5;244m",  # Dark gray
    "\033[38;5;232m"   # Black
]

VERTICAL_PADDING = 2
HORIZONTAL_PADDING = 3
STEP_SIZE = 9
BAR_WIDTH = 4

class Stats:
    def __init__(self, main_window_size, main_window_pos):
        self.win = curses.newwin(main_window_size[0], main_window_size[1], main_window_pos[0], main_window_pos[1])
        self.win.bkgd(' ', curses.color_pair(2))
        self.state = "week"
        for i, color_index in enumerate(range(255, 231, -2), start=20):  # Indices de couleurs 255 à 232
            curses.init_pair(i, curses.COLOR_YELLOW, color_index)  # Foreground: Yellow, Background: Gradient
        self.date = datetime.now()
        curses.init_pair(10, 254, curses.COLOR_WHITE)  # Foreground: Light grey, Background: White
   
    def draw(self, data_manager : DataManager):
        if self.state == "month":
            self.draw_month(data_manager)
        else:
            self.draw_week(data_manager)

    def draw_week(self, data_manager : DataManager): 
        stats = data_manager.load_week(self.date.isocalendar().week, self.date.year)
        start_date = datetime.strptime(stats[0][0], "%d/%m/%Y")
        end_date = datetime.strptime(stats[6][0], "%d/%m/%Y")
        week_info_str = f"week from {start_date.strftime('%B')} {start_date.day}th to {end_date.strftime('%B')} {end_date.day}th"
        self.win.addstr(0, 20, week_info_str)
        stats = [float(seconds) / 3600 for _, seconds in stats]

        yx = self.win.getbegyx()
        maxyx = self.win.getmaxyx()

        for i in range(yx[0], maxyx[0]):
            if i % VERTICAL_PADDING != 0:
                self.win.addstr(i - 1, yx[1] + HORIZONTAL_PADDING, "|")
            else:
                self.win.addstr(i + 1, yx[1] + 1, f"{12 - i:2}┼")
                # Fill the window with a very long light gray string
                if(i < maxyx[0] - VERTICAL_PADDING):
                    long_string = "─" * (maxyx[1] - yx[1] - HORIZONTAL_PADDING*2)
                    self.win.addstr(i + 1, yx[1] + 4, long_string, curses.color_pair(10))

        for i in range(yx[1], maxyx[1] - HORIZONTAL_PADDING):
            if i % STEP_SIZE != 0:
                self.win.addstr(maxyx[0] - VERTICAL_PADDING, i, "─")
            elif i > yx[1] + HORIZONTAL_PADDING:
                self.win.addstr(maxyx[0] - VERTICAL_PADDING, i, "┴")
                day_index = (i // STEP_SIZE) % len(days) - 1
                day_label = days[day_index][:3]
                self.win.addstr(maxyx[0] - 1, i - 1, day_label)
        

        first_x = ((yx[1] + HORIZONTAL_PADDING) // STEP_SIZE + 1) * STEP_SIZE
        for x, i in enumerate(range(first_x, maxyx[1] - HORIZONTAL_PADDING, STEP_SIZE)):
            for y in range(maxyx[0] - VERTICAL_PADDING, maxyx[0] - int(stats[x])-VERTICAL_PADDING, -1):
                if y == maxyx[0] - int(stats[x])-VERTICAL_PADDING +1 and int(stats[x]) != 1:
                    self.win.addstr(y, i - 1, "▄" * BAR_WIDTH)
                elif y == maxyx[0] - VERTICAL_PADDING:
                    self.win.addstr(y, i - 1, "▀" * BAR_WIDTH)
                else:
                    self.win.addstr(y, i - 1, "█" * BAR_WIDTH)
                    
        self.win.addstr(maxyx[0] - VERTICAL_PADDING, yx[1] + HORIZONTAL_PADDING, "┼")

        self.win.refresh()

    def draw_month(self, data_manager : DataManager):
        self.win.clear()
        maxyx = self.win.getmaxyx()
        yx = self.win.getbegyx()

        # Calculate grid dimensions
        grid_width = (maxyx[1] - HORIZONTAL_PADDING // 2) // 7
        grid_height = (maxyx[0] - VERTICAL_PADDING // 2) // 5

        # Get the current month and year
        today = datetime.now()
        current_month = today.month
        current_year = today.year

        stats = data_manager.load_month(self.date.month, self.date.year)
        # Extract the first and last weekday numbers from the stats array
        first_weekday = datetime.strptime(stats[0][0], "%d/%m/%Y").weekday()
        days_in_month = len(stats)
        stats = [float(seconds) / 3600 for _, seconds in stats]

        # Load stats for the current month
        # Write the days of the week on the second line (y-axis 2)
        for i, day in enumerate(days):
            x_pos = HORIZONTAL_PADDING + i * grid_width + grid_width // 2
            self.win.addstr(1, x_pos, day[:2])

        # Draw the grid and fill each square with the day of the month
        day_counter = 1
        for week in range(6):  # Maximum 6 weeks overlap in a month
            for day in range(7):  # 7 days in a week
                if week == 0 and day < first_weekday:
                    continue  # Skip days before the first day of the month
                if day_counter > days_in_month:
                    break  # Stop if all days of the month are filled

                x_pos = HORIZONTAL_PADDING + day * grid_width + grid_width // 2
                y_pos = VERTICAL_PADDING + week * grid_height + grid_height // 2 -1
                day_time = stats[day_counter - 1]
                color_id = int(day_time + 20)
                self.win.addstr(y_pos, x_pos - 3, "   ", curses.color_pair(color_id))  # Left padding
                self.win.addstr(y_pos, x_pos + 2, "    ", curses.color_pair(color_id))  # Right padding
                self.win.addstr(y_pos + 1, x_pos - 3, "         ", curses.color_pair(color_id))  # Bottom padding
                self.win.addstr(y_pos, x_pos, str(day_counter).zfill(2), curses.color_pair(color_id))
                day_counter += 1

        # Add the name of the month at position (0, 20)
        month_name = self.date.strftime("%B")
        year = self.date.year
        self.win.addstr(0, 32, f"{month_name} {year}")
        self.win.refresh()

    def handleInput(self, cmd):
        if cmd == "month":
            self.state = "month"
        elif cmd == "week":
            self.state = "week"
        if cmd == "[C":  # Right arrow key
            if self.state == "week":
                self.date = self.date + timedelta(days=7)
            elif self.state == "month":
                next_month = self.date.replace(day=28) + timedelta(days=4)  # Go to next month
                self.date = next_month.replace(day=1)  # Set to the first day of the next month
        elif cmd == "[D":  # Left arrow key
            if self.state == "week":
                self.date = self.date - timedelta(days=7)
            elif self.state == "month":
                prev_month = self.date.replace(day=1) - timedelta(days=1)  # Go to the last day of the previous month
                self.date = prev_month.replace(day=1)  # Set to the first day of the previous month