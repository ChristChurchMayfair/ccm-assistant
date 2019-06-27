import unittest
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

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


class TestGetSermon(unittest.TestCase):
    def test_get_morning_sermon_three_weeks_ago(self):
        timestamp_now: str = datetime.utcnow().replace(tzinfo=timezone.utc,
                                                       microsecond=0).isoformat().replace("+00:00", "Z")
        requested_sermon_date: str = "2019-06-09" #(datetime.now() - timedelta(21)).date().isoformat()
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
                                                    "name": "Evening",
                                                    "id": "EVENING"
                                                }
                                            }
                                        ],
                                        "authority": TEST_AUTHORITY
                                    }
                                ]
                            },
                            "name": "Service",
                            "value": "evening",
                            "confirmationStatus": "NONE"
                        },
                    },
                    "name": "PlaySermon",
                    "confirmationStatus": "NONE"
                },
                "requestId": TEST_REQUEST_ID,
                "type": "IntentRequest"
            },
            "context": {
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
        }
        import json
        print(json.dumps(alexa_main.lambda_handler(event, None)))
