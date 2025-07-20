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
<img width="330" height="127" alt="image" src="https://github.com/user-attachments/assets/a2988e6d-ad2b-4a72-8dd3-6ed511185f86" />
<img width="330" height="127" alt="image" src="https://github.com/user-attachments/assets/7d4e6909-7a02-4979-9fba-279f4c05771c" />
<img width="330" height="127" alt="image" src="https://github.com/user-attachments/assets/40e986d6-78ac-4c62-aaab-4eb298f61b90" />


## Requirements

Before running the application, ensure you have the following:

*   **Python 3.6 or higher**: The application is written in Python 3.
*   **`curses` Library**: This library is usually pre-installed on Linux and macOS. For Windows, you might need to install it.
*   **JSON Files**: The application reads and writes data to JSON files.

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

## Running the Application

1.  **Navigate to the Project Directory**:

    ```bash
    cd pomodoro_timer_v2
    ```

2.  **Run the Application**:

    ```bash
    python3 src/application.py
    ```

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
*   `month` : dksplay monthly work hours
*   `week` : go back to weekly work hours
*   `timer` : go back to pomorodo clock from stats window

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
