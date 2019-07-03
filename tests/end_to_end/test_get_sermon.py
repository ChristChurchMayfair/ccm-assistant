import unittest
from datetime import datetime, timezone, timedelta
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


class TestGetSermon(unittest.TestCase):
    def test_get_morning_sermon_future(self):
        requested_sermon_date: str = (datetime.now() + timedelta(7)).date().isoformat()
        service_name: str = "Morning"
        service_id: str = "MORNING"
        service_value: str = "morning"
        event = {
            "session": test_session,
            "version": test_version,
            "request": {
                "locale": "en-GB",
                "timestamp": timestamp_now,
                "dialogState": "STARTED",
                "intent": {
                    "slots": {
                        "Date": {
                            "name": "Date",
                            "source": "USER",
                            "value": requested_sermon_date,
                            "confirmationStatus": "NONE"
                        },
                        "Service": {
                            "source": "USER",
                            "resolutions": {
                                "resolutionsPerAuthority": [
                                    {
                                        "status": {
                                            "code": "ER_SUCCESS_MATCH"
                                        },
                                        "values": [
                                            {
                                                "value": {
                                                    "name": service_name,
                                                    "id": service_id
                                                }
                                            }
                                        ],
                                        "authority": TEST_AUTHORITY
                                    }
                                ]
                            },
                            "name": "Service",
                            "value": service_value,
                            "confirmationStatus": "NONE"
                        },
                    },
                    "name": "PlaySermon",
                    "confirmationStatus": "NONE"
                },
                "requestId": TEST_REQUEST_ID,
                "type": "IntentRequest"
            },
            "context": test_context
        }
        response: Dict[str, Any] = alexa_main.lambda_handler(event, {})
        self.assertEqual(response["response"]["outputSpeech"], {
            "type": "PlainText",
            "text": "That service hasn't happened yet! "
        })
        self.assertTrue(response["response"]["shouldEndSession"])

    def test_get_evening_sermon_three_weeks_ago(self):
        requested_sermon_date: str = (datetime.now() - timedelta(21)).date().isoformat()
        service_name: str = "Evening"
        service_id: str = "EVENING"
        service_value: str = "evening"
        event = {
            "session": test_session,
            "version": test_version,
            "request": {
                "locale": "en-GB",
                "timestamp": timestamp_now,
                "dialogState": "STARTED",
                "intent": {
                    "slots": {
                        "Date": {
                            "name": "Date",
                            "source": "USER",
                            "value": requested_sermon_date,
                            "confirmationStatus": "NONE"
                        },
                        "Service": {
                            "source": "USER",
                            "resolutions": {
                                "resolutionsPerAuthority": [
                                    {
                                        "status": {
                                            "code": "ER_SUCCESS_MATCH"
                                        },
                                        "values": [
                                            {
                                                "value": {
                                                    "name": service_name,
                                                    "id": service_id
                                                }
                                            }
                                        ],
                                        "authority": TEST_AUTHORITY
                                    }
                                ]
                            },
                            "name": "Service",
                            "value": service_value,
                            "confirmationStatus": "NONE"
                        },
                    },
                    "name": "PlaySermon",
                    "confirmationStatus": "NONE"
                },
                "requestId": TEST_REQUEST_ID,
                "type": "IntentRequest"
            },
            "context": test_context
        }
        response: Dict[str, Any] = alexa_main.lambda_handler(event, {})

        self.assertEqual(response["response"]["outputSpeech"]["type"], "PlainText")
        self.assertTrue(bool(re.match(r"Here's the sermon, .+, by .+ ", response["response"]["outputSpeech"]["text"])),
                        "The speech output is wrong")
        self.assertEqual(len(response["response"]["directives"]), 1)
        self.assertEqual(response["response"]["directives"][0]["type"], "AudioPlayer.Play")
        self.assertEqual(response["response"]["directives"][0]["playBehavior"], "REPLACE_ALL")
        self.assertTrue(
            bool(re.match(r"https://.+\.mp3", response["response"]["directives"][0]["audioItem"]["stream"]["url"])),
            "The audio stream URL is not an HTTPS URL to an MP3 file")
        self.assertEqual(response["response"]["card"]["type"], "Simple")
        self.assertEqual(type(response["response"]["card"]["title"]), str)
        self.assertEqual(type(response["response"]["card"]["content"]), str)
