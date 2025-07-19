import json
from datetime import date
from datetime import timedelta
from src.helper import print_debug

class DataManager:
    """
    A class to manage data stored in JSON files, organized by year. 
    Provides methods to load and update data for specific days, weeks, or months.
    Initialize the DataManager with the folder path where JSON files are stored.
    Args:
        path_folder (str): The folder path containing the JSON files.
    """
    def __init__(self, path_folder: str):
        self.path_folder = path_folder
    
    def load_week(self, week_nbr, year) -> list[tuple[str, int]]:
        """
        Load data for a specific week of a given year.
        Args:
            week_nbr (int): The ISO week number (1-53).
            year (int): The year for which to load the data.
        Returns:
            list: A list of tuples containing the date (str) and its corresponding time (int).
                  Returns an empty list if no data is found for the week.
        """
        # Get the absolute path of the JSON file
        year_path_file = self.path_folder + str(year) + ".json"
        week_data = []
        try:
            with open(year_path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        start_date = date.fromisocalendar(year, int(week_nbr), 1)
        for i in range(7):
            key = (start_date + timedelta(days=i)).strftime("%d/%m/%Y")
            if key in data:
                week_data.append((key,data[key]))
            else:
                week_data.append((key, 0))
    
        return week_data
    
    def load_month(self, month_nbr, year) -> list[tuple[str, int]]:
        """
        Load data for a specific month of a given year.
        Args:
            month_nbr (int): The month number (1-12).
            year (int): The year for which to load the data.
        Raises:
            ValueError: If the month number is not between 1 and 12.
        Returns:
            list: A list of tuples containing the date (str) and its corresponding time (int).
                  Returns an empty list if no data is found for the month.
        """
        if not 1 <= month_nbr <= 12:
            raise ValueError("Invalid month number. Must be between 1 and 12.")
        
        year_path_file = self.path_folder + str(year) + ".json"
       
        month_data = []
        try:
            with open(year_path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        
        start_date = date(year, int(month_nbr), 1)
        days_in_month = (date(year, int(month_nbr) + 1, 1) - timedelta(days=1)).day if month_nbr < 12 else 31

        for i in range(days_in_month):
            key = (start_date + timedelta(days=i)).strftime("%d/%m/%Y")
            if key in data:
                month_data.append((key,data[key]))
            else:
                month_data.append((key, 0))

        return month_data
    
    def load_day(self, day_nbr, month_nbr, year) -> tuple[str, int]:
        """
        Load data for a specific day.
        Args:
            day_nbr (int): The day number (1-31).
            month_nbr (int): The month number (1-12).
            year (int): The year for which to load the data.
        Returns:
            tuple: A tuple containing the date (str) and its corresponding time (int).
                   Returns None if the file does not exist or the date is not found.
        """
        # Build the key in the format "dd/mm/yyyy"
        year_path_file = self.path_folder + str(year) + ".json"
        
        try:
            with open(year_path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}  # Return None if the file does not exist

        key = f"{day_nbr:02}/{month_nbr:02}/{year}"
        return (key, data.get(key, 0))  # Return the value for the key or None if not found
    
    def set_day(self, day_nbr, month_nbr, year, time):
        """
        Set or overwrite data for a specific day.
        Args:
            day_nbr (int): The day number (1-31).
            month_nbr (int): The month number (1-12).
            year (int): The year for which to set the data.
            time (int): The value to set for the day, typically representing seconds.
        Returns:
            None
        """
        # Build the key in the format "dd/mm/yyyy"
        year_path_file = self.path_folder + str(year) + ".json"
        
        try:
            with open(year_path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
            with open(year_path_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        key = f"{day_nbr:02}/{month_nbr:02}/{year}"
        data[key] = time  # Assuming the value is an integer representing seconds

        with open(year_path_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update_day(self, day_nbr, month_nbr, year, time: int):
        """
        Update data for a specific day by adding the given time to the existing value.
        Args:
            day_nbr (int): The day number (1-31).
            month_nbr (int): The month number (1-12).
            year (int): The year for which to update the data.
            time (int): The value to add to the existing data, typically representing seconds.
        Returns:
            None
        """
        # Build the key in the format "dd/mm/yyyy"
        year_path_file = self.path_folder + str(year) + ".json"
        
        try:
            with open(year_path_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
            with open(year_path_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        key = f"{day_nbr:02}/{month_nbr:02}/{year}"
        if key in data:
            data[key] += time  # Assuming the value is an integer representing seconds
        else:
            data[key] = time  # Initialize with the given time

        with open(year_path_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)