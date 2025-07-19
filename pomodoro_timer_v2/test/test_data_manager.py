import unittest
from src.data_manager import DataManager
import os

class TestApp(unittest.TestCase):
    # Initialize shared attributes for the test class
    week_data = [
        ("21/07/2025", 28800),
        ("22/07/2025", 7200),
        ("23/07/2025", 25200),
        ("24/07/2025", 0),
        ("25/07/2025", 28800),
        ("26/07/2025", 3600),
        ("27/07/2025", 7200),
    ]
    month_data = [
        ("01/06/2025", 14400),
        ("03/06/2025", 7200),
        ("05/06/2025", 3600),
        ("07/06/2025", 0),
        ("10/06/2025", 25200),
        ("12/06/2025", 28800),
        ("15/06/2025", 5400),
        ("18/06/2025", 7200),
        ("20/06/2025", 0),
        ("22/06/2025", 3600),
        ("25/06/2025", 28800),
        ("28/06/2025", 25200)
    ]

    dataManager = DataManager("test/test_data/work_time_")

    def test_load_week(self):
        # Access attributes initialized in setUp
        val = self.dataManager.load_week(30, 2025)
        self.assertEqual(val, self.week_data)  # Example assertion

    def test_load_month(self):
        val = self.dataManager.load_month(6, 2025)
        self.assertEqual(val, self.month_data)

    def test_load_day(self):
        val = self.dataManager.load_day(21, 7, 2025)
        self.assertEqual(val, self.week_data[0])

    def test_update_day(self):
        self.dataManager.update_day(22, 7, 2025, 800)
        val = self.dataManager.load_day(22, 7, 2025)
        self.assertEqual(val, (self.week_data[1][0], self.week_data[1][1] + 800))
        self.dataManager.set_day(22, 7, 2025, 7200)
    

    def test_set_day_creates_new_file(self):
        # Set a random date for the year 2026
        random_date = (15, 8, 2026)  # 15th August 2026
        file_path = "test/test_data/work_time_2026.json"

        # Set the day and check if the file is created
        self.dataManager.set_day(*random_date, 3600)
        self.assertTrue(os.path.exists(file_path))

        # Clean up by deleting the file
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_update_day_creates_new_file(self):
        # Update a random date for the year 2026
        random_date = (20, 9, 2026)  # 20th September 2026
        file_path = "test/test_data/work_time_2026.json"

        # Update the day and check if the file is created
        self.dataManager.update_day(*random_date, 7200)
        self.assertTrue(os.path.exists(file_path))

        # Clean up by deleting the file
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    unittest.main()