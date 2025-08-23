from src.timer import PomodoroTimer  
from src.data_manager import DataManager
import curses
import threading
import time
import curses
from src.stats import Stats
from datetime import datetime

main_window_size = (14, 70)
main_window_pos = (0,0)
cmd_window_size = (3, 70)
cmd_window_pos = (14, 0)

class Application:
    def __init__(self):
        today = datetime.now()
        self.state = "timer"
        self.data_manager = DataManager("data/work_time_")
        self.cmd_handler = CmdHandler(cmd_window_size, cmd_window_pos, self)
        self.timer = PomodoroTimer(main_window_size, main_window_pos, self.cmd_handler)
        self.timer.total_work_time = self.data_manager.load_day(today.day, today.month, today.year)[1]
        self.stats = Stats(main_window_size, main_window_pos)
        self.refresh_queue = []

    def main(self):
        self.refresh_queue.append(self.timer.draw)
        listener = threading.Thread(target=self.cmd_handler.handle_input, daemon=True)
        display = threading.Thread(target=self.draw, daemon=True)
        listener.start()
        display.start()
        try:
            while listener.is_alive():
                self.timer.update()

                if(self.state == 'timer'):
                    self.refresh_queue.append(self.timer.draw)
                time.sleep(1)
        except KeyboardInterrupt:
            curr_date = datetime.now()
            self.data_manager.set_day(curr_date.day, curr_date.month, curr_date.year, int(self.timer.total_work_time))

    def draw(self):
        while True:
            while self.refresh_queue:
                func = self.refresh_queue.pop(0)
                func()
            time.sleep(1)
    
class CmdHandler:
    """
    A class to handle command-line input and manage the application's state and interactions.
    This class is responsible for creating a command window, handling user input, and updating
    the application's state based on the commands entered. It interacts with other components
    of the application, such as the timer and stats modules, to perform the required actions.
    """

    def __init__(self, cmd_window_size, cmd_window_pos, application: Application):
        self.application = application
        self.win = curses.newwin(cmd_window_size[0], cmd_window_size[1], cmd_window_pos[0], cmd_window_pos[1]) 
        self.draw()

    def draw(self):
        self.win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.win.bkgd(' ', curses.color_pair(0))
        self.win.addstr(1, 1, "cmd: ")

    def help(self):
        """
        Set the work and break durations for the Pomodoro timer.
        Prompts the user to input the work and break durations in the format "work-break".
        Updates the timer's work mode and remaining time based on the input.
        """
        # Prompt the user for input
        self.win.addstr(1, 1, "cmd: refresh-next-pause;stats-month-week-left arrow-right arrow")
        self.win.refresh()
        self.win.getstr(1, 29).decode("utf-8").strip()

        
    def handle_input(self):

        while True:
            self.application.refresh_queue.append(self.win.refresh)

            curses.echo()  # Activer l'écho pour afficher les caractères saisis
            cmd = self.win.getstr(1, 6).decode("utf-8").strip()  # Lire la commande
            curses.noecho()

            if(cmd in 'stats'):
                curr_date = datetime.now()
                self.application.state = 'stats'
                #update work time data file to display correct stats
                self.application.data_manager.set_day(curr_date.day, curr_date.month, curr_date.year, self.application.timer.total_work_time)
                self.application.refresh_queue.append(self.application.timer.win.clear)
                self.application.refresh_queue.append(lambda: self.application.stats.draw(self.application.data_manager))
            elif(cmd in 'timer'):
                self.application.state = 'timer'
                self.application.stats.state = 'week'
                self.application.refresh_queue.append(self.application.stats.win.clear)

            elif cmd == 'refresh':
                self.application.refresh_queue.append(self.win.clear)
                self.application.refresh_queue.append(self.draw)
                if self.application.state == 'timer':
                    self.application.refresh_queue.append(self.application.timer.win.clear)
                elif self.application.state == 'stats':
                    self.application.refresh_queue.append(self.application.stats.win.clear)
                    self.application.refresh_queue.append(self.application.stats.draw)
            elif cmd == 'help':
                self.help()
            elif self.application.state == "timer":
                self.application.timer.handleInput(cmd)

            elif self.application.state == 'stats':
                self.application.stats.handleInput(cmd)
                self.application.refresh_queue.append(self.application.stats.win.clear)
                self.application.refresh_queue.append(lambda: self.application.stats.draw(self.application.data_manager))
            
            self.win.move(1, 6)
            _, w = self.win.getmaxyx()
            # Clear only the input area, preserving borders
            self.win.addstr(1, 6, " " * (w - 7))
            
            time.sleep(1)
            
if __name__ == "__main__":
    def run_app(stdscr):
        app = Application()
        app.main()
        #app.cmd_handler.win.getch()  # Wait for user input before exiting

    curses.wrapper(run_app)

#add hour on each column
#if hour decimal bigger than .75 round up
#for mean month and week work hour compute only mean until current day whole week/month.
