# Pomodoro Timer Application
## Overview

This is a command-line Pomodoro Timer application built with Python and the `curses` library. It helps you manage your work and break intervals to boost productivity. The application provides a visual interface in the terminal, displaying the timer, statistics, and controls.

## Features

*   **Pomodoro Timer**: Manages work and break intervals.
*   **Customizable**: Allows setting custom work and break durations.
*   **Statistics**: Tracks total work time and completed cycles.
*   **Visual Interface**: Uses `curses` for a terminal-based user interface.
*   **Data Persistence**: Saves work time data to JSON files.
*   **Color Gradients**: Uses ANSI escape codes and curses color pairs for visual appeal.
*   **Break window**: Open a full screen firefox window at the end of a cycle. (may use alt f4 to close it)

<img width="330" height="127" alt="Capture d’écran du 2026-01-15 19-21-17" src="https://github.com/user-attachments/assets/a7f9c9c4-b5c7-411d-859d-7bf69025b1a9" />
<img width="330" height="127" alt="Capture d’écran du 2026-01-15 19-21-26" src="https://github.com/user-attachments/assets/416d2a1a-228e-4a78-be5f-058de0d1f544" />
<img width="330" height="127" alt="image" src="https://github.com/user-attachments/assets/bd3b3964-b0a4-4d7e-9409-8fc02cc510bc" />
<img width="260" height="127" alt="image" src="https://github.com/user-attachments/assets/a8908c4d-29bf-4250-9857-70e3cc62824c" />

## Application Tutorial

### Initializing the Application

When you start the application, it initializes the `curses` environment and sets up the main window. The `Stats` and `PomodoroTimer` classes are instantiated to manage the timer and statistics.

### Main Screen Layout

The main screen is divided into several sections:

*   **Timer Display**: Shows the remaining time in the current phase (work or break).
*   **Statistics**: Displays total work time and completed cycles.
*   **Controls**: commands line interface.

### Using the Pomodoro Timer

1.  **Starting and Pausing the Timer**:

    *   Press `p` to start or pause the timer.

2.  **Switching Between Work and Break**:

    *   The timer automatically switches between work and break phases.

3.  **Customizing the Timer**:

    *   You can customize the work and break durations.

4.  **Viewing Statistics**:

    *   The total work time and completed cycles are displayed on the screen on weekly or monthly basis.

### Available Commands

The following commands are available during runtime:

*   `pause`: Pause the timer.
*   `next`: skip current working phase
*   `resume`: resume the timer
*   `ctrl^c`: Quit the application.
*   `help`: Display all commands.
*   `stats` : go in stat window, display weekly work hours
*   `<-,->`: navigate in monthy or weekly stats
*   `month` : display monthly work hours
*   `week` : go back to weekly work hours
*   `timer` : go back to pomorodo clock from stats window
*   `set` : can set current work time. the app will prompt you to enter time.
*   `mode` : change work/break duration. the app will prompt you to enter new mode.
We can enter partial commands and it will guess closest one. For e.g "n" instead of "next", or "r" or "res" instead of "resume"

### Data Storage

The application stores work time data in JSON files located in the `data` directory. Each file is named according to the year (e.g., `work_time_2025.json`). The data is organized by date, with each date associated with the total work time in seconds.

Example `work_time_2025.json` file:

```json
{
    "20/07/2025": 4242,
    "21/07/2025": 28800,
    "22/07/2025": 7200,
    "23/07/2025": 25200,
    "24/07/2025": 0,
    "25/07/2025": 28800,
    "26/07/2025": 3600,
    "27/07/2025": 7200,
    "28/07/2025": 3600,
    "29/07/2025": 5400,
    "30/07/2025": 7200,
    "31/07/2025": 25200
}

```

## Compatibility
The main branch is compatible with **Linux**.

for **MAC OS and Windows** please use the **windows-macOS** branch. 
This other version does not have the break pop-up at the end of a cycle.

## Requirements

Before running the application, ensure you have the following:

*   **Python 3.6 or higher**: The application is written in Python 3.
*   **`curses` Library**: This library is usually pre-installed on Linux and macOS. For Windows, you might need to install it.
*   **firefox**: The app opens a break firefox window when work time is finished.

### Installing Dependencies

1.  **Check Python Version**:

    ```bash
    python3 --version
    ```

2.  **Install `curses` (if needed)**:

    *   **Linux**: Usually pre-installed.
    *   **macOS**: Usually pre-installed.
    *   **Windows**:

        *   Install the `windows-curses` package:

            ```bash
            pip install windows-curses
            ```

    *   `datetime` (usually pre-installed)
    *   `json` (usually pre-installed)
    *   `curses` (see above for installation instructions)
3. **Install firefox**:
    sudo apt install firefox

## Running the Application

1.  **Navigate to the Project Directory**:

    ```bash
    cd pomodoro_timer_v2
    ```

2.  **Run the Application**:

    ```bash
    python3 src/application.py
    ```
## Convenient Launch
create a pomodoro.sh file with this script :
```bash
cd <path-to-folder>/pomodoro-timer/pomodoro_timer_v2
python3 application.py
```

make it executable :
```
chmod +x pomodoro.sh
```

You can now open terminal and launch 
```
./pomodoro.sh
```

