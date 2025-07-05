import time
import sys
import threading
import re

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
    def __init__(self):
        self.total_work_time = 0        # secondes de travail total
        self.remaining_time = 0    # secondes restantes dans la phase
        self.state = 'work'      # 'work', 'break', 'paused', 'overtime'
        self.isPaused = True
        self.overwork_time = 0
        self.isovertime = False
        self.work_mode = (50, 10)  # (minutes_travail, minutes_pause)
        self.cycles_completed = 0
        self.last_time_update = time.time()

    def set_work_mode(self, mode_tuple):
        self.work_mode = mode_tuple

    def start(self):
        self.state = 'work'
        self.remaining_time = self.work_mode[0] * 60
        self.last_time_update = time.time()

    def pause(self):
        if self.state in ('work', 'break'):
            self.isPaused = True

    def resume(self):
        self.isPaused = False
        # on reprend la phase en cours
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
        self.last_time_update = now

        if self.isPaused != True:
            if not self.isovertime:
                self.remaining_time -= elapsed
            if self.state == 'work':
                self.total_work_time += elapsed

        if self.remaining_time <= 0 and self.state == 'work' and not self.isovertime:
            self.cycles_completed += 1
            self.isovertime = True
            self.remaining_time = 0
        
        if self.isovertime:
            self.overwork_time += elapsed

    
    def draw_ui(self):
        # choix du temps de référence
        phase_minutes = self.work_mode[0] if self.state == 'work' else self.work_mode[1]

        pct_progress_bar = int((self.remaining_time * 100) / (phase_minutes * 60))
        progress_bar_len = 20
        filled = int((pct_progress_bar * progress_bar_len) / 100)
        empty = progress_bar_len - filled


        total_work_time_str = remaining_time_str = time.strftime("%H:%M:%S", time.gmtime(int(self.total_work_time)))
        remaining_time_str = time.strftime("%M:%S", time.gmtime(int(self.remaining_time)))
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

        print(f"       {CLR_CYAN}             {CLR_BLACK}POMODORO CLOCK{CLR_CYAN}")
        print(f"       {CLR_BLACK}        ╚═══════════════════╝")
        print(f"       {CLR_CYAN}╔═{display_mode}═════════════════════╗ {CLR_CYAN}┌[mode]┐")
        
        print(f"       {CLR_GREEN}║ [{progress_bar}] {pct_progress_bar:3d}%    ║{CLR_GREEN}=║  {CLR_YELLOW}{self.work_mode[0]:02d}  ║")
        
        print(f"       {CLR_RESET}║ ➜            {remaining_time_str}    {CLR_GREEN}{over_time_str}   ║=║  {CLR_YELLOW}{self.work_mode[1]:02d}  ║")
        
        print(f"       {CLR_CYAN}╚══════╔══════╔═══════╔══════╔═══╝ {CLR_CYAN}└──────┘")
        print(f"       {CLR_CYAN}┌─────────────────┐┌─────────────────┘───┘─┐")
        
        print(f"       │ {CLR_GREEN}Pomodoros: {CLR_RESET}{self.cycles_completed:3d}  ││ {CLR_GREEN}Total Work: {total_work_time_str}  │")
        print(f"       {CLR_CYAN}└─────────────────┘└───────────────────────┘")
        print(f"cmd : ")
        #print(f"{CLR_BLACK}\n  pause| resume| skip| reset| mode| quit |save |load : {CLR_RESET}", end="", flush=True)

def input_listener(pomodoro: PomodoroTimer):
    while True:
        cmd = input().strip().lower()
        if cmd == "pause":
            pomodoro.pause()
        elif cmd == "resume":
            pomodoro.resume()
        elif cmd == "skip":
            if pomodoro.state == "work":
                pomodoro.begin_break()
            else:
                pomodoro.begin_work()
        elif cmd == "reset":
            pomodoro.discard()
            pomodoro.start()
        elif cmd == "mode":
            # exemple : on bascule entre 25|5 et 50|10
            while True:
                mode_input = input("Enter new mode in format 'a-b' (e.g., 25-5): ").strip()
                if re.match(r'^\d+-\d+$', mode_input):
                    a, b = map(int, mode_input.split('-'))
                    pomodoro.set_work_mode((a, b))
                    break
                else:
                    print("Invalid format. Please use 'a-b' where a and b are numbers.")
            pomodoro.start()
        elif cmd in ("quit", "q"):
            break
        
def main():
    pomodoro = PomodoroTimer()
    pomodoro.start()

    listener = threading.Thread(target=input_listener, args=(pomodoro,), daemon=True)
    listener.start()

    try:
        while listener.is_alive():
            pomodoro.update()
            pomodoro.draw_ui()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    print("\nPomodoro timer stopped.")

if __name__ == "__main__":
    main()