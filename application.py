from timer import PomodoroTimer
import curses
import threading
import time
import curses
from stats import Stats

main_window_size = (14, 70)
main_window_pos = (0,0)
cmd_window_size = (3, 70)
cmd_window_pos = (14, 0)

class Application:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.state = "timer"
        self.cmd_handler = CmdHandler(cmd_window_size, cmd_window_pos, self)
        self.timer = PomodoroTimer(main_window_size, main_window_pos, self.cmd_handler)
        self.stats = Stats(main_window_size, main_window_pos)
        self.refresh_queue = []

    def main(self):
        listener = threading.Thread(target=self.cmd_handler.handle_input, daemon=True)
        display = threading.Thread(target=self.refresh, daemon=True)
        listener.start()
        display.start()
        try:
            while listener.is_alive():
                self.timer.update()

                if(self.timer.total_work_time % 60 == 0):
                    self.stats.write_new_stats(self.timer.total_work_time)
                    
                if(self.state == 'timer'):
                    self.refresh_queue.append(self.timer.draw)
                # Attente qun_week_state le lock soit libéré
                time.sleep(1)
        except KeyboardInterrupt:
            self.stats.write_new_stats(self.timer.total_work_time)

        print("\nPomodoro timer stopped.")

    def refresh(self):
        while True:
            while self.refresh_queue:
                func = self.refresh_queue.pop(0)
                func()
            time.sleep(1)
    
class CmdHandler:
    def __init__(self, cmd_window_size, cmd_window_pos, application: Application):
        self.application = application
        self.win = curses.newwin(cmd_window_size[0], cmd_window_size[1], cmd_window_pos[0], cmd_window_pos[1]) 
        self.draw()

    def draw(self):
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
                self.application.refresh_queue.append(self.application.stats.draw)
            elif(cmd == 'timer'):
                self.application.state = 'timer'
                self.application.refresh_queue.append(self.application.stats.win.clear)

            elif cmd == 'refresh':
                self.application.refresh_queue.append(self.win.clear)
                self.application.refresh_queue.append(self.draw)
                if self.application.state == 'timer':
                    self.application.refresh_queue.append(self.application.timer.win.clear)
                    self.application.refresh_queue.append(self.application.timer.draw)
                elif self.application.state == 'stats':
                    self.application.refresh_queue.append(self.application.stats.win.clear)
                    self.application.refresh_queue.append(self.application.stats.draw)

            elif self.application.state == "timer":
                self.application.timer.handleInput(cmd)

            elif self.application.state == 'stats':
                self.application.stats.handleInput(cmd)
                self.application.refresh_queue.append(self.application.stats.win.clear)
                self.application.refresh_queue.append(self.application.stats.draw)
            
            self.win.move(1, 6)
            _, w = self.win.getmaxyx()
            # Clear only the input area, preserving borders
            self.win.addstr(1, 6, " " * (w - 7))
            
            time.sleep(1)
            
if __name__ == "__main__":
    def run_app(stdscr):
        app = Application(stdscr)
        app.main()
        app.cmd_handler.win.getch()  # Wait for user input before exiting

    curses.wrapper(run_app)

#test stats display transition between years
#update stats.csv
#compute mean work time per week
#monthly heat map
#secret cmd to set hour time work
#secret cmd to load worked time