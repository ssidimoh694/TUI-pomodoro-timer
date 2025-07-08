from timer import PomodoroTimer
import curses
import threading
import time
import curses
from stats import Stats

class Application:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.timer = PomodoroTimer(stdscr)
        self.state = "timer"
        self.cmd_handler = CmdHandler(self)
        self.stats = Stats(self)
        self.refresh_queue = []

    def main(self):
        listener = threading.Thread(target=self.cmd_handler.handle_input, daemon=True)
        display = threading.Thread(target=self.refresh, daemon=True)
        listener.start()
        display.start()
        try:
            while listener.is_alive():
                self.timer.update()
                if(self.state == 'timer'):
                    self.refresh_queue.append(self.timer.draw)
                if(self.state == 'stats'):
                    self.refresh_queue.append(self.stats.draw)
                # Attente que le lock soit libéré
                time.sleep(1)
        except KeyboardInterrupt:
            pass

        print("\nPomodoro timer stopped.")

    def refresh(self):
        while True:
            while self.refresh_queue:
                func = self.refresh_queue.pop(0)
                func()
            time.sleep(1)
    
class CmdHandler:
    def __init__(self, application: Application):
        self.application = application
        self.win = curses.newwin(3, 70, 14, 0) 
        self.win.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.win.bkgd(' ', curses.color_pair(0))
        self.win.addstr(1, 1, "cmd: ")

    def handle_input(self):

        while True:
            self.application.refresh_queue.append(self.win.refresh)
            curses.echo()  # Activer l'écho pour afficher les caractères saisis
            cmd = self.win.getstr(1, 6).decode("utf-8").strip()  # Lire la commande
            curses.noecho()
            if(cmd == 'stats'):
                self.application.state = 'stats'
                self.application.refresh_queue.append(self.application.timer.win.clear)
            elif(cmd == 'timer'):
                self.application.state = 'timer'
                self.application.refresh_queue.append(self.application.stats.win.clear)


            elif self.application.state == "timer":
                self.application.timer.handleInput(cmd)

            elif self.application.state == 'stats':
                self.application.stats.handleInput(cmd)
            
            self.win.move(1, 6)
            _, w = self.win.getmaxyx()
            # Clear only the input area, preserving borders
            self.win.addstr(1, 6, " " * (w - 7))
            
            time.sleep(1)
            
if __name__ == "__main__":
    def run_app(stdscr):
        app = Application(stdscr)
        app.main()

    curses.wrapper(run_app)