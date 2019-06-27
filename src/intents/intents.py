import utils
import resources.bible as bible
import resources.passages as passages
import resources.sermons as sermons
import resources.events as events
import config
import cards
import speech
from .intents_utils import ensure_date_and_service_slots_filled, ensure_date_is_a_sunday, \
    ensure_service_valid, ensure_date_is_not_in_the_future


def handle_welcome(_intent):
    speech_output = speech.WELCOME
    should_end_session = False
    reprompt_text = None
    return utils.build_response(
        utils.build_speechlet_response(card_title=cards.WELCOME_TITLE,
                                       card_text=cards.WELCOME_CONTENT, output=speech_output,
                                       reprompt_text=reprompt_text,
                                       should_end_session=should_end_session))


def handle_session_end_request(_intent):
    should_end_session = True
    return utils.build_response(
        utils.build_speechlet_response(card_title=cards.END_SESSION_TITLE,
                                       card_text=cards.END_SESSION_CONTENT,
                                       output=speech.END_SESSION, reprompt_text=None,
                                       should_end_session=should_end_session))


def handle_get_passage(intent):
    maybe_response = ensure_date_and_service_slots_filled(intent)
    if maybe_response:
        return maybe_response

    date, maybe_response = ensure_date_is_a_sunday(
        intent,
        future_days_go_back_year_threshold=config.FUTURE_DAYS_GO_BACK_YEAR_THRESHOLD_PASSAGES)
    if maybe_response:
        return maybe_response

    service, maybe_response = ensure_service_valid(intent)
    if maybe_response:
        return maybe_response

    reading_data = passages.get_passage(date, service)
    if not reading_data:
        speechlet_response = utils.build_speechlet_response(output=speech.NO_BIBLE_PASSAGE,
                                                            reprompt_text=None,
                                                            should_end_session=True)
        return utils.build_response(speechlet_response)

    book = reading_data["book"]
    start_chapter = str(reading_data["start"]["chapter"])
    start_verse = str(reading_data["start"]["verse"])
    end_chapter = str(reading_data["end"]["chapter"])
    end_verse = str(reading_data["end"]["verse"])
    humanised_passage = utils.humanise_passage(book, start_chapter, start_verse, end_chapter,
                                               end_verse)
    passage_text = bible.get_bible_text(book, start_chapter, start_verse, end_chapter, end_verse)

    get_read_passage_directives = [{"type": "Dialog.ElicitSlot", "slotToElicit": "ReadPassage"}]

    if "value" not in intent["slots"]["ReadPassage"]:
        should_end_session = False

        speechlet_response = utils.build_speechlet_response(
            card_title=cards.get_passage_title(date, service),
            card_text=cards.GET_PASSAGE_CONTENT.format(
                passage_text=passage_text, passage=humanised_passage,
                bible_translation=config.BIBLE_TRANSLATION
            ),
            output=speech.BIBLE_PASSAGE_RESPONSE.format(bible_passage=humanised_passage),
            reprompt_text=None, should_end_session=should_end_session,
            directives=get_read_passage_directives)

        return utils.build_response(speechlet_response)

    try:
        to_read_passage = intent["slots"]["ReadPassage"]["resolutions"]["resolutionsPerAuthority"][
                              0]["values"][0]["value"]["id"] == "YES"
    except KeyError:
        speech_output = speech.PLEASE_REPEAT_GENERAL
        speechlet_response = utils.build_speechlet_response(output=speech_output,
                                                            reprompt_text=None,
                                                            should_end_session=False,
                                                            directives=get_read_passage_directives)
        return utils.build_response(speechlet_response)

    speech_output = (
        speech.READ_RESPONSE.format(
            passage_text=bible.remove_square_bracketed_verse_numbers(passage_text))
        if to_read_passage
        else speech.DO_NOT_READ_RESPONSE
    )

    speechlet_response = utils.build_speechlet_response(output=speech_output, reprompt_text=None,
                                                        should_end_session=True)
    return utils.build_response(speechlet_response)


def handle_get_next_event(_intent):
    reprompt_text = None
    should_end_session = True
    next_event = events.get_next_event()

    if not next_event:
        return utils.build_response(utils.build_speechlet_response(
            output=speech.NO_EVENTS_FOUND,
            reprompt_text=reprompt_text,
            should_end_session=should_end_session))

    return utils.build_response(utils.build_speechlet_response(
        output=speech.get_next_event(event_name=next_event['name'],
                                     event_datetime=next_event['datetime']),
        reprompt_text=reprompt_text,
        should_end_session=should_end_session,
        card_text=cards.get_next_event_content(
            event_description=next_event['description'],
            event_location_name=next_event['location_name']),
        card_title=cards.get_next_event_title(
            event_title=next_event['name'],
            event_datetime=next_event['datetime']),
        card_small_image_url=next_event['small_image_url'],
        card_large_image_url=next_event['large_image_url']))


def handle_play_sermon(intent):
    maybe_response = ensure_date_and_service_slots_filled(intent)
    if maybe_response:
        return maybe_response

    date, maybe_response = ensure_date_is_a_sunday(
        intent,
        future_days_go_back_year_threshold=config.FUTURE_DAYS_GO_BACK_YEAR_THRESHOLD_SERMONS)
    if maybe_response:
        return maybe_response

    service, maybe_response = ensure_service_valid(intent)
    if maybe_response:
        return maybe_response

    maybe_response = ensure_date_is_not_in_the_future(date)
    if maybe_response:
        return maybe_response

    sermon = sermons.get_sermon(date, service)

    if not sermon:
        return utils.build_response(utils.build_speechlet_response(
            output=speech.SERMON_NOT_AVAILABLE, reprompt_text=None, should_end_session=True))

    reprompt_text = None
    should_end_session = True
    return utils.build_response(
        utils.build_audio_player_play_response(
            output_speech=speech.SERMON_PREAMBLE.format(sermon_title=sermon["title"],
                                                        speaker=sermon["speaker"]),
            reprompt_text=reprompt_text, audio_stream_url=sermon["audio_url"],
            should_end_session=should_end_session,
            card_content=cards.GET_SERMON_CONTENT.format(passage=sermon["passage"],
                                                         series_name=sermon["series_name"],
                                                         speaker=sermon["speaker"]),
            card_title=cards.GET_SERMON_TITLE.format(sermon_title=sermon["title"])))
