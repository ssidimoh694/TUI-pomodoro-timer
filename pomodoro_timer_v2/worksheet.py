from datetime import datetime
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
def main():
    dict = load_json_stats()
    print(dict['16/07/25'])

def write_new_stats(total_work):

        today = datetime.now()
        day_name = today.strftime("%A")
        date_str = today.strftime("%d/%m/%y")
        try:
            with open("stats.csv", 'r+b') as f:
                f.seek(0, 2)  # Move to the end of the file
                f.seek(-2, 1)
                while f.read(1) != b'\n':  # Find the start of the last line
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

def loadWeekStats(n_week_stat):
        try:
            with open("stats.csv", 'rb') as f:
                f.seek(0, 2)
                stats = []
                for i in range(n_week_stat):
                    while f.tell() > 0:
                        beg_of_line = f.seek(-2, 1)
                        while f.tell() > 0 and f.read(1) != b'\n':
                            beg_of_line = f.seek(-2, 1)
                        line = f.readline().decode().strip()
                        f.seek(beg_of_line, 0)
                        if(i == n_week_stat -1):
                            stats.append(line.split(','))
                            if "eow" in line:
                                break
            stats.reverse()
            return (stats[1:], str(stats[0] + 1).split(',')[1])
        except FileNotFoundError:
            return None

from datetime import datetime, timedelta
import json

def loadMonthsStats(month):
    try:
        with open("stats.csv", 'rb') as f:
            f.seek(0, 2)
            stats = []
            while f.tell() > 0:
                beg_of_line = f.seek(-2, 1)
                while f.tell() > 0 and f.read(1) != b'\n': 
                    beg_of_line = f.seek(-2, 1)
                line = f.readline().decode().strip()
                f.seek(beg_of_line, 0)
                line = line.split(',')
                if len(line) == 1:
                    continue
                row_month = int(line[1].split('/')[1])
                if row_month == month:
                    stats.append(line)
                elif row_month < month:
                    break
            stats.reverse()
        return stats
    except FileNotFoundError:
        return None

def load_json_stats():
    try:
        with open("stats_dict.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
# Example usage

if __name__ == "__main__":
    main()