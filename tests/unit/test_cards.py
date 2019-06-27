import unittest
from datetime import date, datetime

import cards


class TestCards(unittest.TestCase):
    def test_get_passage_title(self):
        morning = "morning"
        evening = "evening"
        self.assertEqual(cards.get_passage_title(date(2012, 4, 21), morning),
                         "Bible reading for 21st April 2012 AM service")
        self.assertEqual(cards.get_passage_title(date(1997, 6, 2), evening),
                         "Bible reading for 2nd June 1997 PM service")
        self.assertEqual(cards.get_passage_title(date(2018, 6, 3), evening),
                         "Bible reading for 3rd June 2018 PM service")
        self.assertEqual(cards.get_passage_title(date(2018, 7, 4), evening),
                         "Bible reading for 4th July 2018 PM service")
        self.assertEqual(cards.get_passage_title(date(2018, 11, 13), morning),
                         "Bible reading for 13th November 2018 AM service")
        self.assertEqual(cards.get_passage_title(date(2018, 12, 11), morning),
                         "Bible reading for 11th December 2018 AM service")

    def test_get_next_event_title(self):
        test_event_datetime = datetime(2000, 1, 1, 4, 20, 33)
        self.assertEqual(cards.get_next_event_title("Mission Breakfast", test_event_datetime),
                         "Mission Breakfast - 04:20, Saturday 01 January")

    def test_get_next_event_content(self):
        self.assertEqual(cards.get_next_event_content("", "The Moon"), "The Moon")
        self.assertEqual(cards.get_next_event_content("Brunch for Women", "Christ Church Mayfair"),
                         "Brunch for Women\nLocation: Christ Church Mayfair")
