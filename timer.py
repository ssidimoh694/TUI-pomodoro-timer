import time
import sys
import threading
import re
import curses
from helper import print_debug
import math
# Définir vos constantes de couleur ici
CLR_RESET  = "\033[0m"
CLR_BLACK  = "\033[30m"
CLR_RED    = "\033[31m"
CLR_GREEN  = "\033[32m"
CLR_YELLOW = "\033[33m"
CLR_BLUE   = "\033[34m"
CLR_MAGENTA= "\033[35m"
CLR_CYAN   = "\033[36m"
CLR_WHITE  = "\033[37m"

class PomodoroTimer:
    def __init__(self, stdscr):

        self.total_work_time = 0        # secondes de travail total
        self.remaining_time = 0    # secondes restantes dans la phase
        self.state = 'work'      # 'work', 'break', 'paused', 'overtime'
        self.isPaused = True
        self.overwork_time = 0
        self.isovertime = False
        self.work_mode = (50, 10)  # (minutes_travail, minutes_pause)
        self.cycles_completed = 0
        self.last_time_update = 0
        self.state = 'work'
        self.remaining_time = self.work_mode[0] * 60

        self.win = curses.newwin(14, 70, 0, 0)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.win.bkgd(' ', curses.color_pair(2))
        curses.curs_set(0)

    def set_work_mode(self, mode_tuple):
        self.work_mode = mode_tuple
        
    def pause(self):
        if self.state in ('work', 'break'):
            self.isPaused = True

    def resume(self):
        self.isPaused = False
        self.last_time_update = time.time()

    def discard(self):
        self.remaining_time = 0
        self.state = 'paused'
    
    def begin_break(self):
        self.state = "break"
        self.remaining_time = self.work_mode[1] * 60
        self.overwork_time = 0
        self.last_time_update = time.time()

    def begin_work(self):
        self.state = "work"
        self.remaining_time = self.work_mode[0] * 60
        self.overwork_time = 0
        self.last_time_update = time.time()

    def update(self):
        now = time.time()
        elapsed = now - self.last_time_update
        print_debug(f" elapsed : {elapsed}")
        if self.isPaused != True:
            if not self.isovertime:
                self.remaining_time -= elapsed
                print_debug(f"remaining time : {self.remaining_time}")
            if self.state == 'work':
                self.total_work_time += elapsed
                print_debug(f"added total work : {self.total_work_time}")

        if self.remaining_time <= 0 and self.state == 'work' and not self.isovertime:
            self.cycles_completed += 1
            self.isovertime = True
            self.remaining_time = 0
        
        if self.isovertime:
            self.overwork_time += elapsed

        self.last_time_update = now


    def handleInput(self, cmd):
        if cmd == "next":
            if self.state == "work":
                self.begin_break()
            elif self.state == "break":
                self.begin_work()
        if cmd == "pause":
            self.pause()
        elif cmd == "resume":
            self.resume()
        elif cmd == "skip":
            if self.state == "work":
                self.begin_break()
            else:
                self.begin_work()
        elif cmd == "reset":
            self.discard()
        elif cmd == "mode":
            # exemple : on bascule entre 25|5 et 50|10
            while True:
                mode_input = input("Enter new mode in format 'a-b' (e.g., 25-5): ").strip()
                if re.match(r'^\d+-\d+$', mode_input):
                    a, b = map(int, mode_input.split('-'))
                    self.set_work_mode((a, b))
                    break
                else:
                    print("Invalid format. Please use 'a-b' where a and b are numbers.")
    
    def draw(self):
        self.win.border('|', '|', '-', '-', '+', '+', '+', '+')
        # choix du temps de référence
        phase_minutes = self.work_mode[0] if self.state == 'work' else self.work_mode[1]

        pct_progress_bar = int((self.remaining_time * 100) / (phase_minutes * 60))
        progress_bar_len = 20
        filled = int((pct_progress_bar * progress_bar_len) / 100)
        empty = progress_bar_len - filled


        total_work_time_str = time.strftime("%H:%M:%S", time.gmtime(math.ceil(self.total_work_time)))
        remaining_time_str = time.strftime("%M:%S", time.gmtime(math.floor(self.remaining_time)))
        progress_bar = ("." * empty) + ("#" * filled)

        display_mode = '[' + self.state.upper() 
        if self.isPaused:
            display_mode += "(P)" + ']'
            display_mode += "═" if self.state == 'work' else ""
        else:
            display_mode += ']'
            display_mode += "════" if self.state == 'work' else "═══"

        if self.isovertime:
            over_time_str = '+' + time.strftime("%M:%S", time.gmtime(int(self.overwork_time)))
        else: 
            over_time_str = '      '
        y = 3
        x = 6
        self.win.addstr(1, x, "                    POMODORO CLOCK", curses.color_pair(2) | curses.A_BOLD)
        self.win.addstr(y, x,f"       ╔═{display_mode}═════════════════════╗ ┌[mode]┐", curses.color_pair(2))
        y+=1
        self.win.addstr(y, x,f"       ║ [{progress_bar}] {pct_progress_bar:3d}%    ║=║  {self.work_mode[0]:02d}  ║", curses.color_pair(2))
        y+=1
        self.win.addstr(y, x,f"       ║ ➜            {remaining_time_str}    {over_time_str}   ║=║  {self.work_mode[1]:02d}  ║", curses.color_pair(2))
        y+=1    
        self.win.addstr(y, x,f"       ╚══════╔══════╔═══════╔══════╔═══╝ └──────┘", curses.color_pair(2))
        y+=1
        self.win.addstr(y, x,f"       ┌─────────────────┐┌─────────────────┘───┘─┐", curses.color_pair(2))
        y+=1
        self.win.addstr(y, x,f"       │ Pomodoros: {self.cycles_completed:3d}  ││ Total Work: {total_work_time_str}  │", curses.color_pair(2))
        y+=1
        self.win.addstr(y, x,f"       └─────────────────┘└───────────────────────┘", curses.color_pair(2))
        y+=1
        self.win.refresh()
