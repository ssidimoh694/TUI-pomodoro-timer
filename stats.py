import curses
from datetime import datetime

days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
max_height = 24        # 24 rows == 12h at ½h precision
col_w = 4              # each day‐column is 4 chars wide
x0 = 6                 # leave room for Y axis labels
y0 = 1 
class Stats:
    def __init__(self, application):
        self.win = curses.newwin(14, 70, 0, 0)
        self.win.bkgd(' ', curses.color_pair(2))
        #self.win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.stats_file_path = "stats.csv"


    def drawa(self):
        self.win.addstr(1, 1, "Stats")
        self.win.refresh()
    
    def draw(self):
        self.win.addstr(1, 1, "^", curses.A_BOLD)
        for i in range(1, 13):
            self.win.addstr(i + 1, 1, "║")

        self.win.addstr(13, 68, ">", curses.A_BOLD)

        self.win.addstr(13, 1, "╚")
        for i in range(1, 67):
            self.win.addstr(13, i + 1, "═")

        # for x in range(7):
        #     for y in range(11):
        #         self.win.addstr(x*5 + 2, y, "I$$I")
        for x in range (6, 66, 9):
            self.win.addstr(1, x , "╔════╗")
            for y in range(2, 13):
                self.win.addstr(y, x, "║::::║")

        self.win.refresh()

        

    def drawv2(self):
        # load last week stats into a dict
        stats = dict(self.loadWeekStats())
        
        max_height = 24        # 24 rows == 12h at ½h precision
        col_w = 4              # each day‐column is 4 chars wide
        x0 = 6                 # leave room for Y axis labels
        y0 = 1                 # top margin

        # Draw Y axis: every 2h == every 4 rows
        for i in range(max_height + 1):
            y = y0 + i
            # label every 4th row with hours remaining
            if i % 4 == 0:
                hours = (max_height - i) // 2
                self.win.addstr(y, 0, f"{hours:2d}")
            else:
                self.win.addstr(y, 0, "  ")
                # vertical axis line
                self.win.addstr(y, 3, "|")

        # Draw top border of columns
        for dx in range(col_w * len(days)):
            self.win.addch(y0, x0 + dx, "_")

        # Draw each day‐column
        for idx, day in enumerate(days):
            total = float(stats.get(day, 0))
            blocks = min(int(total * 2), max_height)
            col_x = x0 + idx * col_w
            # fill from bottom up
            for b in range(blocks):
                y = y0 + max_height - b
                self.win.addstr(y, col_x, "I$$I")
                # draw the day label under the column (3 letter abbrev)
                label = day[:3].center(col_w)
                self.win.addstr(y0 + max_height + 1, col_x, label)

        self.win.refresh()

    def add_new_stats(self, total_work):
        with open(self.stats_file_path, 'a') as file:
            date = datetime.now().strftime("%A")
            file.write(f"{date},{total_work}\n")

    def loadWeekStats(self):
        week_stats = []
        try:
            with open(self.stats_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    day, work = line.strip().split(',')
                    week_stats.append((day, work))
                    if day == "Monday":
                        break
        except FileNotFoundError:
            pass
        return week_stats
    
    def handleInput(cmd):
        pass

# Exemple d'utilisation avec curses
def main(stdscr):
    curses.curs_set(0)
    stats = Stats()
    stats.draw()
    stdscr.getch()  # Attendre une entrée pour quitter