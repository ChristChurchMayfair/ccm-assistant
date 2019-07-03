import unittest
from datetime import datetime, timezone
from typing import Dict, Any
import re

import alexa_main
from config import APPLICATION_ID

TEST_USER_ID: str = "tEsTuSeR123"
TEST_REQUEST_ID: str = "rEqUeStId123"
TEST_SESSION_ID: str = "tEsTsEsH123"
TEST_AUTHORITY: str = "tEsTaUtHoRiTy"
TEST_DEVICE_ID: str = "tEsTdEvIcEiD"
TEST_API_ACCESS_TOKEN: str = "tEsTaPiAcCeSsToKeN"

test_session: Dict[str, Any] = {
    "new": True,
    "sessionId": TEST_SESSION_ID,
    "user": {
        "userId": TEST_USER_ID
    },
    "application": {
        "applicationId": APPLICATION_ID
    }
}

test_version: str = "1.0"
test_context: Dict[str, Any] = {
    "AudioPlayer": {
        "token": "https://cdn.com/talk.mp3",
        "playerActivity": "STOPPED",
        "offsetInMilliseconds": 1234
    },
    "System": {
        "device": {
            "deviceId": TEST_DEVICE_ID,
            "supportedInterfaces": {
                "AudioPlayer": {}
            }
        },
        "application": {
            "applicationId": APPLICATION_ID
        },
        "apiAccessToken": TEST_API_ACCESS_TOKEN,
        "user": {
            "userId": TEST_USER_ID
        },
        "apiEndpoint": "https://api.eu.amazonalexa.com"
    }
}
timestamp_now: str = datetime.utcnow().replace(tzinfo=timezone.utc, microsecond=0).isoformat().replace("+00:00", "Z")


class TestGetNextEvent(unittest.TestCase):
    def test_get_next_event(self):
        event = {
            "session": test_session,
            "version": test_version,
            "request": {
                "locale": "en-GB",
                "timestamp": timestamp_now,
                "dialogState": "STARTED",
                "intent": {
                    "name": "GetNextEvent",
                    "confirmationStatus": "NONE"
                },
                "requestId": TEST_REQUEST_ID,
                "type": "IntentRequest"
            },
            "context": test_context
        }
        response: Dict[str, Any] = alexa_main.lambda_handler(event, {})
        self.assertEqual(response["response"]["outputSpeech"]["type"], "PlainText")
        self.assertEqual(type(response["response"]["outputSpeech"]["text"]), str)
        self.assertTrue(bool(re.match(r"The next event is .+ on \w+ \d+ \w+ at \d\d?:\d\d?( in the evening)?. ",
                                      response["response"]["outputSpeech"]["text"])), "The speech output is wrong")
        self.assertTrue(response["response"]["shouldEndSession"])
        self.assertTrue(bool(re.match(r".+ - \d\d:\d\d, \w+ \d\d \w+", response["response"]["card"]["title"])),
                        "The card title is wrong")
        self.assertIn(response["response"]["card"]["type"], {"Standard", "Simple"})
        card_text: str = (response["response"]["card"]["content"]
                          if response["response"]["card"]["type"] == "Simple"
                          else response["response"]["card"]["text"])
        self.assertTrue(bool(re.match(r".+\nLocation: .+", card_text)), "The card text is wrong")
