import unittest
from datetime import datetime

import speech


class TestSpeech(unittest.TestCase):
    def test_get_next_event_morning(self):
        test_event_datetime = datetime(2016, 11, 13, 9, 14, 15)
        self.assertEqual(speech.get_next_event("Tasty breakfast!", test_event_datetime),
                         "The next event is Tasty breakfast! on Sunday 13 November at 9:14. ")

    def test_get_next_event_afternoon(self):
        test_event_datetime = datetime(2019, 12, 23, 15, 21, 30)
        self.assertEqual(speech.get_next_event("Afternoon tea", test_event_datetime),
                         "The next event is Afternoon tea on Monday 23 December at 3:21. ")

    def test_get_next_event_evening(self):
        test_event_datetime = datetime(2019, 12, 23, 20, 15, 0)
        self.assertEqual(speech.get_next_event("Evening of fun", test_event_datetime),
                         "The next event is Evening of fun on Monday 23 December at 8:15 in the evening. ")
