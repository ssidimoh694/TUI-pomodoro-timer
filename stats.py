import curses
from datetime import datetime, timedelta, date
from helper import print_debug
import csv

days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]

day_to_number = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}
VERTICAL_PADDING = 2
HORIZONTAL_PADDING = 3
STEP_SIZE = 9
BAR_WIDTH = 4
class Stats:
    def __init__(self, main_window_size, main_window_pos):
        self.win = curses.newwin(main_window_size[0], main_window_size[1], main_window_pos[0], main_window_pos[1])
        self.win.bkgd(' ', curses.color_pair(2))
        self.stats_file_path = "stats.csv"

        self.curr_week = datetime.now().isocalendar().week
        self.curr_year = datetime.now().year
        self.weeks_in_curr_year = date(self.curr_year, 12, 28).isocalendar().week

        self.current_week_stats_display = self.curr_week
        self.current_year_stats_display = self.curr_year
        self.weeks_in_curr_year_display = self.weeks_in_curr_year

    def draw(self): 
        stats = self.loadWeekStats()
        stats = [(day, float(seconds) / 3600) for day, _, seconds in stats]
        for day in days:
            index = day_to_number[day] - 1
            if index >= len(stats) or stats[index][0] != day:
                stats.insert(index, (day, 0))
        yx = self.win.getbegyx()
        maxyx = self.win.getmaxyx()

        for i in range(yx[0], maxyx[0]):
            if i % VERTICAL_PADDING != 0:
                self.win.addstr(i - 1, yx[1] + HORIZONTAL_PADDING, "|")
            else:
                self.win.addstr(i + 1, yx[1] + 1, f"{12 - i:2}┼")

        for i in range(yx[1], maxyx[1] - HORIZONTAL_PADDING):
            if i % STEP_SIZE != 0:
                self.win.addstr(maxyx[0] - VERTICAL_PADDING, i, "─")
            elif i > yx[1] + HORIZONTAL_PADDING:
                self.win.addstr(maxyx[0] - VERTICAL_PADDING, i, "┼")
                day_index = (i // STEP_SIZE) % len(days) - 1
                day_label = days[day_index][:3]
                self.win.addstr(maxyx[0] - 1, i - 1, day_label)
        
        first_x = ((yx[1] + HORIZONTAL_PADDING) // STEP_SIZE + 1) * STEP_SIZE
        for x, i in enumerate(range(first_x, maxyx[1] - HORIZONTAL_PADDING, STEP_SIZE)):
            for y in range(maxyx[0] - VERTICAL_PADDING, maxyx[0] - int(stats[x][1])-VERTICAL_PADDING, -1):
                self.win.addstr(y, i - 1, "▒" * BAR_WIDTH)
                    
        self.win.addstr(maxyx[0] - VERTICAL_PADDING, yx[1] + HORIZONTAL_PADDING, "┼")
        self.win.addstr(0, 20,get_week_interval(self.current_week_stats_display))
        self.win.refresh()

    def write_new_stats(self, total_work):

        today = datetime.now()
        day_name = today.strftime("%A")
        date_str = today.strftime("%d/%m/%y")
        try:
            with open(self.stats_file_path, 'r+b') as f:
                f.seek(0, 2) 
                while f.read(1) != b'\n':
                    f.seek(-2, 1)
                beg_of_line = f.tell()
                last_line = f.readline().decode().strip()
                last_line = last_line.split(',') if last_line else None

                if last_line:
                    prev_num = day_to_number[last_line[0]]
                    curr_num = day_to_number[day_name]

                    if last_line[1] == date_str:
                        f.seek(beg_of_line)
                        f.write(f"{day_name},{date_str},{total_work}\n".encode())
                        return
                    elif curr_num <= prev_num:
                        f.seek(0, 2)
                        f.write(f"eow\n".encode())
                
                f.seek(0, 2)
                f.write(f"{day_name},{date_str},{total_work}\n".encode())

        except FileNotFoundError:
            pass

    def loadWeekStats(self):
        try:
            with open(self.stats_file_path, 'rb') as f:
                f.seek(0, 2)
                stats = []
                year_diff = self.curr_year - self.current_year_stats_display
                total_weeks = 0

                # Calculate the total number of weeks from the current year to the target year
                for year in range(self.current_year_stats_display, self.curr_year + 1):
                    weeks_in_year = date(year, 12, 31).isocalendar().week
                    print_debug(f"Year: {year}, Weeks in year: {weeks_in_year}")

                    if year == self.curr_year:
                        total_weeks += self.curr_week - self.current_week_stats_display + 1
                        print_debug(f"Adding weeks for curr_year: {self.curr_week}")
                    elif year == self.current_year_stats_display:
                        total_weeks += weeks_in_year - self.current_week_stats_display + 1
                        print_debug(f"Adding weeks for current_year_stats_display: {weeks_in_year - self.current_week_stats_display + 1}")
                    else:
                        total_weeks += weeks_in_year
                        print_debug(f"Adding weeks for intermediate year: {weeks_in_year}")
                print_debug(str(total_weeks))
                for i in range(total_weeks):
                    while f.tell() > 0:
                        beg_of_line = f.seek(-2, 1)
                        while f.tell() > 0 and f.read(1) != b'\n': 
                            beg_of_line = f.seek(-2, 1)
                        line = f.readline().decode().strip()
                        f.seek(beg_of_line, 0)
                        if line == "eow":
                            break
                        if i == year_diff * self.weeks_in_curr_year + self.curr_week - self.current_week_stats_display:
                            stats.append(line.split(','))
            stats.reverse()
            return stats
        except FileNotFoundError:
            return None
    
    def handleInput(self, cmd):
        if cmd == "[C":  # Right arrow key
            print_debug(f"Right arrow pressed. Current week: {self.current_week_stats_display}, Weeks in current year: {self.weeks_in_curr_year}")
            if self.current_week_stats_display < self.weeks_in_curr_year and self.current_week_stats_display < self.curr_week:
                self.current_week_stats_display += 1
            print_debug(f"Incremented week. New current week: {self.current_week_stats_display}")
        elif cmd == "[D":  # Left arrow key
            if self.current_week_stats_display > 1:
                self.current_week_stats_display -= 1
            else:
                self.current_year_stats_display -= 1
                self.weeks_in_curr_year_display = date(self.current_year_stats_display -1 - 1, 12, 31).isocalendar().week
                self.current_week_stats_display = self.weeks_in_curr_year_display

def get_week_interval(week_number):
    # Find the first day of the year
    year = datetime.now().year
    first_day_of_year = datetime(year, 1, 1)
    
    # Find the first Monday of the year (ISO week starts on Monday)
    first_monday = first_day_of_year + timedelta(days=(7 - first_day_of_year.weekday()) % 7)
    
    # Calculate the start date of the given week
    start_date = first_monday + timedelta(weeks=week_number - 1)
    
    # Calculate the end date of the given week (Sunday)
    end_date = start_date + timedelta(days=6)
    
    return f"week from {start_date.strftime('%B')} {start_date.day}th to {end_date.strftime('%B')} {end_date.day}th"

