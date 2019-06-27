import json
from typing import Dict, Any


import config
import handlers.events as events


def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    # Log input event to CloudWatch
    print("EVENT OBJECT:\n{event_json}".format(event_json=json.dumps(event)))

    # Make sure only this Alexa skill can use this function
    application_id: str = (
        event["session"]["application"]["applicationId"]
        if "session" in event.keys()
        else event["context"]["System"]["application"]["applicationId"])
    if application_id != config.APPLICATION_ID:
        raise ValueError("Invalid Application ID")

    request_type = event["request"]["type"]

    if request_type == "LaunchRequest":
        return events.on_launch()
    elif request_type == "IntentRequest":
        return events.on_intent(event["request"], event["context"])
