from typing import Dict, Any, List

get_read_passage_directives: List[Dict[str, str]] = [{"type": "Dialog.ElicitSlot", "slotToElicit": "ReadPassage"}]


def is_date_and_service_slots_filled(intent: Dict[str, Any]) -> bool:
    return "value" in intent["slots"]["Date"] and "value" in intent["slots"]["Service"]


def is_service_valid(intent: Dict[str, Any]) -> bool:
    try:
        _ = intent["slots"]["Service"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"]
        return True
    except KeyError:
        return False


def get_service(intent: Dict[str, Any]) -> str:
    return intent["slots"]["Service"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["id"].lower()

