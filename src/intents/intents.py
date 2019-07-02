import datetime
from typing import Any, Dict, Optional

import utils
import resources.bible as bible
import resources.passages as passages
import resources.sermons as sermons
import resources.events as events
import config
import cards
import speech
from intents.intents_utils import is_date_and_service_slots_filled, is_service_valid, get_service,\
    get_read_passage_directives
from custom_types import AlexaResponse


def handle_welcome(_intent: Any = None) -> AlexaResponse:
    return utils.build_speechlet_response(speech.WELCOME, False, card_title=cards.WELCOME_TITLE,
                                          card_text=cards.WELCOME_CONTENT)


def handle_session_end_request(_intent: Any = None) -> AlexaResponse:
    return utils.build_speechlet_response(speech.END_SESSION, True, card_title=cards.END_SESSION_TITLE,
                                          card_text=cards.END_SESSION_CONTENT)


def handle_get_passage(intent) -> AlexaResponse:
    if not is_date_and_service_slots_filled(intent):
        return utils.build_delegate_response()

    if not is_service_valid(intent):
        return utils.build_repeat_service_response()

    date: datetime.date = utils.sunday_from(intent["slots"]["Date"]["value"])
    service: str = get_service(intent)

    try:
        reading_data: Dict[str, Any] = passages.get_passage(date, service)
    except RuntimeError as e:
        print(e)
        return utils.build_speechlet_response(speech.NO_BIBLE_PASSAGE_FOR_GIVEN_DATE, True)

    book: str = reading_data["book"]
    start_chapter: str = str(reading_data["start"]["chapter"])
    start_verse: str = str(reading_data["start"]["verse"])
    end_chapter: str = str(reading_data["end"]["chapter"])
    end_verse: str = str(reading_data["end"]["verse"])
    humanised_passage: str = utils.humanise_passage(book, start_chapter, start_verse, end_chapter, end_verse)

    try:
        passage_text: str = bible.get_bible_text(book, start_chapter, start_verse, end_chapter, end_verse)
    except RuntimeError as e:
        print(e)
        return utils.build_speechlet_response(speech.UNABLE_TO_FETCH_BIBLE_PASSAGE, True)

    if "value" not in intent["slots"]["ReadPassage"]:
        card_text: str = cards.format_get_passage_content(passage_text, humanised_passage, config.BIBLE_TRANSLATION)
        return utils.build_speechlet_response(speech.bible_passage_response(humanised_passage), False,
                                              card_title=cards.get_passage_title(date, service), card_text=card_text,
                                              directives=get_read_passage_directives)

    try:
        to_read_passage: bool = intent["slots"]["ReadPassage"]["resolutions"]["resolutionsPerAuthority"][0]["values"][
                                    0]["value"]["id"] == "YES"
    except KeyError:
        return utils.build_speechlet_response(speech.PLEASE_REPEAT_GENERAL, False,
                                              directives=get_read_passage_directives)

    speech_output: str = (bible.remove_square_bracketed_verse_numbers(passage_text)
                          if to_read_passage
                          else speech.DO_NOT_READ_RESPONSE)

    return utils.build_speechlet_response(speech_output, True)


def handle_get_next_event(_intent: Any = None) -> AlexaResponse:
    try:
        next_event: Optional[Dict[str, Any]] = events.get_next_event()
    except RuntimeError as e:
        print(e)
        return utils.build_speechlet_response(speech.NO_EVENTS_FOUND, True)
    if not next_event:
        return utils.build_speechlet_response(speech.NO_EVENTS_FOUND, True)

    output_text: str = speech.get_next_event(event_name=next_event['name'], event_datetime=next_event['datetime'])
    card_title: str = cards.get_next_event_title(event_title=next_event['name'], event_datetime=next_event['datetime'])
    card_text: str = cards.get_next_event_content(event_description=next_event['description'],
                                                  event_location_name=next_event['location_name'])
    return utils.build_speechlet_response(output_text, True, card_text=card_text, card_title=card_title,
                                          card_small_image_url=next_event['small_image_url'],
                                          card_large_image_url=next_event['large_image_url'])


def handle_play_sermon(intent: Dict[str, Any]) -> AlexaResponse:
    if not is_date_and_service_slots_filled(intent):
        return utils.build_delegate_response()

    if not is_service_valid(intent):
        return utils.build_repeat_service_response()

    date: datetime.date = utils.sunday_from(intent["slots"]["Date"]["value"])
    service: str = get_service(intent)

    if not utils.is_not_in_future(date):
        return utils.build_speechlet_response(speech.SERVICE_IS_IN_THE_FUTURE, True)

    try:
        sermon: Optional[Dict[str, str]] = sermons.get_sermon(date, service)
    except RuntimeError as e:
        print(e)
        return utils.build_speechlet_response(speech.SERMON_NOT_AVAILABLE, True)

    if not sermon:
        return utils.build_speechlet_response(speech.SERMON_NOT_AVAILABLE, True)

    preamble: str = speech.sermon_preamble(sermon["title"], sermon["speaker"])
    return utils.build_audio_player_play_response(sermon["audio_url"], True, output_speech=preamble,
                                                  card_content=cards.get_sermon_content(sermon["passage"],
                                                                                        sermon["series_name"],
                                                                                        sermon["speaker"]),
                                                  card_title=sermon["title"])
