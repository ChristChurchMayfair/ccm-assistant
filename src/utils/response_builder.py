import re
from typing import Dict, Any, List, Optional

import config
from requests import Request

import speech
from custom_types import AlexaResponse


def convert_http_mp3_to_https_m3u(http_mp3_url: str) -> str:
    payload: Dict[str, str] = {"url": http_mp3_url}
    dummy_request: Request = Request("GET", config.HTTP_MP3_TO_HTTPS_M3U_API_URL, params=payload).prepare()
    return dummy_request.url


def build_speechlet_response(output: str, should_end_session: bool, directives: Optional[List[Dict[str, Any]]] = None,
                             card_title: Optional[str] = None, card_text: Optional[str] = None,
                             card_small_image_url: Optional[str] = None, card_large_image_url: Optional[str] = None,
                             reprompt_text: Optional[str] = None) -> AlexaResponse:
    speechlet_response: Dict[str, Any] = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }
    if directives:
        speechlet_response["directives"] = directives
    if card_title and card_text:
        card: Dict[str, Any] = {
            "title": card_title
        }
        if card_small_image_url and card_large_image_url:
            card["type"] = "Standard"
            card["text"] = card_text
            card["image"] = {
                "smallImageUrl": card_small_image_url,
                "largeImageUrl": card_large_image_url
            }
        else:
            card["type"] = "Simple"
            card["content"] = card_text

        speechlet_response["card"] = card
    return build_response(speechlet_response)


def build_audio_player_play_response(audio_stream_url: str, should_end_session: bool,
                                     output_speech: Optional[str] = None,
                                     reprompt_text: Optional[str] = None, card_title: Optional[str] = None,
                                     card_content: Optional[str] = None, offset: int = 0) -> AlexaResponse:
    audio_player_response: Dict[str, Any] = {
        "outputSpeech": {
            "type": "PlainText",
            "text": output_speech
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

    audio_stream_url: str = (
        audio_stream_url
        if re.match(r"https://.*", audio_stream_url)
        else convert_http_mp3_to_https_m3u(audio_stream_url))

    directives: List[Dict[str, Any]] = [
        {
            "type": "AudioPlayer.Play",
            "playBehavior": "REPLACE_ALL",
            "audioItem": {
                "stream": {
                    "token": audio_stream_url,
                    "url": audio_stream_url,
                    "offsetInMilliseconds": offset
                }
            }
        }
    ]

    audio_player_response["directives"] = directives

    if card_title and card_content:
        card: Dict[str, str] = {
            "type": "Simple",
            "title": card_title,
            "content": card_content
        }
        audio_player_response["card"] = card

    return build_response(audio_player_response)


def build_audio_player_stop_response() -> AlexaResponse:
    return build_response({
        "outputSpeech": {
            "type": "PlainText",
            "text": None
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": None
            }
        },
        "shouldEndSession": True,
        "directives": [
            {
                "type": "AudioPlayer.Stop"
            }
        ]
    })


def build_delegate_response() -> AlexaResponse:
    return build_response({
        "shouldEndSession": False,
        "directives": [{"type": "Dialog.Delegate"}]
    })


def build_repeat_service_response() -> AlexaResponse:
    return build_speechlet_response(output=speech.PLEASE_REPEAT_SERVICE, should_end_session=False,
                                    directives=[{"type": "Dialog.ElicitSlot", "slotToElicit": "Service"}])


def build_response(response: Dict[str, Any]) -> AlexaResponse:
    return {
        "version": config.RESPONSE_VERSION,
        "response": response
    }
