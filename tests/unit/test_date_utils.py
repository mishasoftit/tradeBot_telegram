import time
import unittest
from datetime import datetime, timedelta
from utils.date_utils import format_timestamp, relative_time

class TestDateUtils(unittest.TestCase):
    def test_format_timestamp_datetime(self):
        """Test formatting with datetime object"""
        dt = datetime(2023, 1, 15, 12, 30, 45)
        result = format_timestamp(dt)
        self.assertEqual(result, "2023-01-15 12:30:45")

    def test_format_timestamp_numeric(self):
        """Test formatting with numeric timestamp"""
        dt = datetime(2023, 1, 15, 12, 30, 45)
        timestamp = time.mktime(dt.timetuple())
        result = format_timestamp(timestamp)
        self.assertEqual(result, "2023-01-15 12:30:45")

    def test_relative_time_just_now(self):
        """Test 'just now' relative time"""
        now = datetime.now()
        result = relative_time(now)
        self.assertEqual(result, "just now")

    def test_relative_time_minutes(self):
        """Test minute-based relative time"""
        now = datetime.now()
        
        # 5 minutes ago
        past = now - timedelta(minutes=5)
        result = relative_time(past)
        self.assertEqual(result, "5 minutes ago")
        
        # 1 minute ago
        past = now - timedelta(minutes=1)
        result = relative_time(past)
        self.assertEqual(result, "1 minute ago")

    def test_relative_time_hours(self):
        """Test hour-based relative time"""
        now = datetime.now()
        
        # 3 hours ago
        past = now - timedelta(hours=3)
        result = relative_time(past)
        self.assertEqual(result, "3 hours ago")
        
        # 1 hour ago
        past = now - timedelta(hours=1)
        result = relative_time(past)
        self.assertEqual(result, "1 hour ago")

    def test_relative_time_days(self):
        """Test day-based relative time"""
        now = datetime.now()
        
        # 2 days ago
        past = now - timedelta(days=2)
        result = relative_time(past)
        self.assertEqual(result, "2 days ago")
        
        # 1 day ago
        past = now - timedelta(days=1)
        result = relative_time(past)
        self.assertEqual(result, "1 day ago")

    def test_relative_time_future(self):
        """Test handling of future timestamps"""
        now = datetime.now()
        future = now + timedelta(minutes=5)
        result = relative_time(future)
        self.assertEqual(result, "just now")  # Falls back to "just now"

if __name__ == '__main__':
    unittest.main()