import unittest

import handlers.events as events
from testing_utils import is_valid_response, ValidResponseObjectTester


class TestEvents(unittest.TestCase):
    def test_on_session_ended_returns_nothing(self):
        self.assertIsNone(events.on_session_ended(None, None))

    def test_on_launch(self):
        response = events.on_launch()
        self.assertTrue(is_valid_response(response))
        response_tester = ValidResponseObjectTester(response)
        self.assertEqual(response_tester.get_speech_plain(),
                         ('I can read you the Bible passage for a service or play you a past sermon. What would you '
                          'like? '))
        self.assertFalse(response_tester.is_session_ending())
        self.assertEqual(response_tester.get_card_text(), ('Hello! Ask me for the bible reading '
                                                           'for a service or a past sermon.'))
        self.assertEqual(response_tester.get_card_title(), 'Christ Church Mayfair')
