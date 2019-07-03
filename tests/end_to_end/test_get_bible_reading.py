import unittest
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
import re

import alexa_main
from config import APPLICATION_ID, MAX_CARD_CHARACTERS

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


class TestGetBibleReading(unittest.TestCase):
    def test_get_bible_passage_coming_sunday_evening_undecided_read(self):
        requested_passage_date: str = (datetime.now() + timedelta(6 - datetime.now().weekday())).date().isoformat()
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
                        "ReadPassage": {
                            "name": "ReadPassage",
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
                        "Date": {
                            "name": "Date",
                            "source": "USER",
                            "value": requested_passage_date,
                            "confirmationStatus": "NONE"
                        },
                    },
                    "name": "GetSermonPassage",
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
        self.assertTrue(len(response["response"]["outputSpeech"]["text"]) > 0, "No speech for Bible passage request")
        self.assertTrue(bool(re.match(r"It's.+\. .*Would you like me to read it out\? ",
                                      response["response"]["outputSpeech"]["text"])), "The speech output is wrong")
        self.assertFalse(response["response"]["shouldEndSession"])
        self.assertEqual(type(response["response"]["directives"]), list)
        self.assertTrue(len(response["response"]["directives"]) > 0)
        self.assertTrue({"type": "Dialog.ElicitSlot", "slotToElicit": "ReadPassage"}
                        in response["response"]["directives"])
        self.assertTrue(bool(re.match(r"Bible reading for \d+[a-z][a-z] \w+ \d\d\d\d \w+ service",
                                      response["response"]["card"]["title"])), "The card title is wrong")
        self.assertTrue(len(response["response"]["card"]["title"]) + len(response["response"]["card"]["content"])
                        <= MAX_CARD_CHARACTERS, "The card is too large")
        self.assertEqual(type(response["response"]["card"]["content"]), str)
        self.assertEqual(type(response["response"]["card"]["title"]), str)
        self.assertEqual(response["response"]["card"]["type"], "Simple")

    def test_get_bible_passage_next_sunday_evening_do_read(self):
        requested_passage_date: str = (datetime.now() + timedelta(13 - datetime.now().weekday())).date().isoformat()
        read_passage_name: str = "Yes"
        read_passage_id: str = "YES"
        read_passage_value: str = "yes"
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
                        "ReadPassage": {
                            "resolutions": {
                                "resolutionsPerAuthority": [
                                    {
                                        "status": {
                                            "code": "ER_SUCCESS_MATCH"
                                        },
                                        "values": [
                                            {
                                                "value": {
                                                    "name": read_passage_name,
                                                    "id": read_passage_id
                                                }
                                            }
                                        ],
                                        "authority": TEST_AUTHORITY
                                    }
                                ]
                            },
                            "name": "ReadPassage",
                            "value": read_passage_value,
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
                        "Date": {
                            "name": "Date",
                            "source": "USER",
                            "value": requested_passage_date,
                            "confirmationStatus": "NONE"
                        },
                    },
                    "name": "GetSermonPassage",
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
        self.assertTrue(len(response["response"]["outputSpeech"]["text"]) > 0, "No speech for Bible passage")
        self.assertTrue(response["response"]["shouldEndSession"])

    def test_get_bible_passage_coming_week_morning_do_not_read(self):
        requested_passage_date: str = (datetime.now() + timedelta(6 - datetime.now().weekday())).date().isoformat()
        read_passage_name: str = "No"
        read_passage_id: str = "NO"
        read_passage_value: str = "no"
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
                        "ReadPassage": {
                            "resolutions": {
                                "resolutionsPerAuthority": [
                                    {
                                        "status": {
                                            "code": "ER_SUCCESS_MATCH"
                                        },
                                        "values": [
                                            {
                                                "value": {
                                                    "name": read_passage_name,
                                                    "id": read_passage_id
                                                }
                                            }
                                        ],
                                        "authority": TEST_AUTHORITY
                                    }
                                ]
                            },
                            "name": "ReadPassage",
                            "value": read_passage_value,
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
                        "Date": {
                            "name": "Date",
                            "source": "USER",
                            "value": requested_passage_date,
                            "confirmationStatus": "NONE"
                        },
                    },
                    "name": "GetSermonPassage",
                    "confirmationStatus": "NONE"
                },
                "requestId": TEST_REQUEST_ID,
                "type": "IntentRequest"
            },
            "context": test_context
        }
        response: Dict[str, Any] = alexa_main.lambda_handler(event, {})

        self.assertEqual(response["response"]["outputSpeech"]["type"], "PlainText")
        self.assertEqual(response["response"]["outputSpeech"]["text"], "Okay ")
        self.assertTrue(response["response"]["shouldEndSession"])
