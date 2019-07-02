import json
from typing import Dict, Any


import config
import events
from custom_types import AlexaResponse


def log_event_to_cloudwatch(event: Dict[str, Any]) -> None:
    print(json.dumps(event))


def validate_application_id(event: Dict[str, Any]) -> None:
    application_id: str = (
        event["session"]["application"]["applicationId"]
        if "session" in event.keys()
        else event["context"]["System"]["application"]["applicationId"])
    if application_id != config.APPLICATION_ID:
        raise ValueError("Invalid Application ID")


def lambda_handler(event: Dict[str, Any], _context: Dict[str, Any]) -> AlexaResponse:
    log_event_to_cloudwatch(event)
    validate_application_id(event)

    request_type: str = event["request"]["type"]

    if request_type == "LaunchRequest":
        return events.on_launch()

    if request_type == "IntentRequest":
        return events.on_intent(event["request"], event["context"])
