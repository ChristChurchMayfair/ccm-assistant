from typing import Dict, Callable, List, Any

import intents

intent_handlers_non_audio: Dict[str, Callable] = {
    "GetSermonPassage": intents.handle_get_passage,
    "PlaySermon": intents.handle_play_sermon,
    "GetNextEvent": intents.handle_get_next_event,
    "AMAZON.HelpIntent": intents.handle_welcome,
    "AMAZON.CancelIntent": intents.handle_session_end_request,
    "AMAZON.StopIntent": intents.handle_session_end_request,
}

irrelevant_audio_intents: List[str] = ["AMAZON.LoopOffIntent", "AMAZON.LoopOnIntent",
                                       "AMAZON.RepeatIntent", "AMAZON.ShuffleOffIntent",
                                       "AMAZON.ShuffleOnIntent", "AMAZON.StartOverIntent",
                                       "AMAZON.PreviousIntent", "AMAZON.NextIntent"]


def on_launch() -> Dict[str, Any]:
    return intents.handle_welcome(None)


def on_intent(intent_request: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    intent: Dict[str, Any] = intent_request["intent"]
    intent_name: str = intent_request["intent"]["name"]

    if intent_name in intent_handlers_non_audio:
        return intent_handlers_non_audio[intent_name](intent)

    # Audio player intents
    if intent_name in irrelevant_audio_intents:
        return intents.handle_irrelevant_audio_intent()
    if intent_name == "AMAZON.PauseIntent":
        return intents.handle_pause()
    if intent_name == "AMAZON.ResumeIntent":
        return intents.handle_resume(context)
    else:
        raise ValueError("Invalid intent")
