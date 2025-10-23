import time
import re
import curses
import math
import subprocess

class PomodoroTimer:
    """
    A class to represent a Pomodoro Timer.
    Attributes:
        cmd_handler: The command handler for managing user input and output.
        total_work_time: Total time spent working in seconds.
        remaining_time: Remaining time in the current phase in seconds.
        state: Current state of the timer ('work', 'break', 'paused', 'overtime').
        isPaused: Boolean indicating if the timer is paused.
        overwork_time: Time spent in overtime in seconds.
        isovertime: Boolean indicating if the timer is in overtime.
        work_mode: Tuple representing work and break durations in minutes.
        cycles_completed: Number of completed Pomodoro cycles.
        last_time_update: Timestamp of the last update.
        win: Curses window object for rendering the timer.
    """
    def __init__(self, main_window_size, main_window_pos, cmd_handler):
        """
        Initialize the PomodoroTimer object.
        Args:
            main_window_size (tuple): Size of the main window (rows, cols).
            main_window_pos (tuple): Position of the main window (y, x).
            cmd_handler: Command handler for managing user input and output.
        """
        self.cmd_handler = cmd_handler
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

        self.win = curses.newwin(main_window_size[0], main_window_size[1], main_window_pos[0], main_window_pos[1])
        self.win.bkgd(' ', curses.color_pair(1))
        curses.curs_set(0)

    def set_work_mode(self):
        """
        Set the work and break durations for the Pomodoro timer.
        Prompts the user to input the work and break durations in the format "work-break".
        Updates the timer's work mode and remaining time based on the input.
        """
        while True:
            # Prompt the user for input
            self.cmd_handler.win.addstr(1, 1, "cmd: Set mode (work-break): ")
            self.cmd_handler.win.refresh()

            # Read user input
            curses.echo()
            user_input = self.cmd_handler.win.getstr(1, 29).decode("utf-8").strip()
            curses.noecho()

            # Validate the input format (e.g., "50-10")
            match = re.match(r"^(\d+)-(\d+)$", user_input)
            if match:
                work_time, break_time = map(int, match.groups())
                # Update remaining time based on the new work mode
                if self.state == 'work':
                    self.remaining_time = work_time * 60
                elif self.state == 'break':
                    self.remaining_time = break_time * 60

                self.work_mode = (work_time, break_time)
                
                # Clear the input area
                self.cmd_handler.win.move(1, 6)
                _, w = self.cmd_handler.win.getmaxyx()
                self.cmd_handler.win.addstr(1, 6, " " * (w - 7))
                self.cmd_handler.win.refresh()
                break
            else:
                self.cmd_handler.win.move(1, 6)
                _, w = self.cmd_handler.win.getmaxyx()
                self.cmd_handler.win.addstr(1, 6, " " * (w - 7))
                self.cmd_handler.win.refresh()

    def set_time(self):
        """
        Set the work and break durations for the Pomodoro timer.
        Prompts the user to input the work and break durations in the format "work-break".
        Updates the timer's work mode and remaining time based on the input.
        """
        while True:
            # Prompt the user for input
            self.cmd_handler.win.addstr(1, 1, "cmd: Set time (hour:min): ")
            self.cmd_handler.win.refresh()

            # Read user input
            curses.echo()
            user_input = self.cmd_handler.win.getstr(1, 29).decode("utf-8").strip()
            curses.noecho()

            # Validate the input format (e.g., "8:10")
            match = re.match(r"^(\d{1,2}):(\d{1,2})$", user_input)
            if match:
                hours, minutes = map(int, match.groups())
                if hours < 24 and minutes < 60:
                    self.total_work_time = hours*3600 + minutes*60
                else:
                    match = None
                
                # Clear the input area
                self.cmd_handler.win.move(1, 6)
                _, w = self.cmd_handler.win.getmaxyx()
                self.cmd_handler.win.addstr(1, 6, " " * (w - 7))
                self.cmd_handler.win.refresh()
                break
            else:
                self.cmd_handler.win.move(1, 6)
                _, w = self.cmd_handler.win.getmaxyx()
                self.cmd_handler.win.addstr(1, 6, " " * (w - 7))
                self.cmd_handler.win.refresh()

    def pause(self):
        if self.state in ('work', 'break'):
            self.isPaused = True

    def resume(self):
        self.isPaused = False
        self.last_time_update = time.time()

    def discard(self):
        self.remaining_time = 0
        self.state = 'paused'
    
    def reset(self):
        self.total_work_time = 0
        self.remaining_time = self.work_mode[0]*60
        self.isPaused = True

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
        if self.isPaused != True:
            if not self.isovertime:
                self.remaining_time -= elapsed
            else:
                self.overwork_time += elapsed
                
            if self.state == 'work':
                self.total_work_time += elapsed

        if self.remaining_time <= 0:
            if self.state == 'work' and not self.isovertime:
                self.cycles_completed += 1
                # Launch Firefox with the break_time.html file
                subprocess.Popen(["firefox", "--new-window", "--kiosk", "/home/anas/Documents/myFiles/devProjects/pomodoro-timer/pomodoro_timer_v2/break_time.html"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.isovertime = True
            self.remaining_time = 0

        self.last_time_update = now

    def handleInput(self, cmd):
        if cmd in "next":
            self.isovertime = False
            if self.state == "work":
                self.begin_break()
            elif self.state == "break":
                self.begin_work()
        if cmd in "pause":
            self.pause()
        elif cmd in "resume":
            self.resume()
        elif cmd in "set":
            self.set_time()
        elif cmd in "reset":
            self.reset()
        elif cmd in "mode":
            self.set_work_mode()
        elif cmd in "help":
            self.help()
    def draw(self):
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
        y = 5
        x = 6
        self.win.addstr(y-3, x, "                    POMODORO CLOCK", curses.color_pair(1) | curses.A_BOLD)
        self.win.addstr(y, x,f"       ╔═{display_mode}═════════════════════╗ ┌[mode]┐", curses.color_pair(1))
        y+=1
        self.win.addstr(y, x,f"       ║ [{progress_bar}] {pct_progress_bar:3d}%    ║=║  {self.work_mode[0]:02d}  ║", curses.color_pair(1))
        y+=1
        self.win.addstr(y, x,f"       ║ ➜            {remaining_time_str}    {over_time_str}   ║=║  {self.work_mode[1]:02d}  ║", curses.color_pair(1))
        y+=1    
        self.win.addstr(y, x,f"       ╚══════╔══════╔═══════╔══════╔═══╝ └──────┘", curses.color_pair(1))
        y+=1
        self.win.addstr(y, x,f"       ┌─────────────────┐┌─────────────────┘───┘─┐", curses.color_pair(1))
        y+=1
        self.win.addstr(y, x,f"       │ Pomodoros: {self.total_work_time/(self.work_mode[0]*60):.1f}  ││ Total Work: {total_work_time_str}  │", curses.color_pair(1))
        y+=1
        self.win.addstr(y, x,f"       └─────────────────┘└───────────────────────┘", curses.color_pair(1))
        y+=1
        self.win.refresh()
