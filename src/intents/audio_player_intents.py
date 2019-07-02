from typing import Any, Dict, Callable

import utils
import speech
from custom_types import AlexaResponse


def handle_irrelevant_audio_intent() -> AlexaResponse:
    return utils.build_speechlet_response(speech.IRRELEVANT_AUDIO_INTENT, True)


handle_pause: Callable[[], AlexaResponse] = utils.build_audio_player_stop_response


def handle_resume(context: Dict[str, Any]) -> AlexaResponse:
    audio_url: str = context["AudioPlayer"]["token"]
    offset: int = context["AudioPlayer"]["offsetInMilliseconds"]
    return utils.build_audio_player_play_response(audio_url, True, offset=offset)
