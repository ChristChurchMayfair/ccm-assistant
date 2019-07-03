from datetime import datetime


IRRELEVANT_AUDIO_INTENT = "I can't do that for a sermon. "
PLEASE_REPEAT_GENERAL = "Sorry, I didn't get that. Please could you repeat that? "
PLEASE_REPEAT_SERVICE = ("Sorry, I didn't get which service you wanted. "
                         "Please could you repeat that? ")
SERVICE_IS_IN_THE_FUTURE = "That service hasn't happened yet! "

# Welcome
WELCOME = ("I can read you the Bible passage for a service or play you a past sermon. "
           "What would you like? ")

# End session
END_SESSION = ""

# Get passage
NO_BIBLE_PASSAGE_FOR_GIVEN_DATE: str = "There isn't a Bible passage for that date "
UNABLE_TO_FETCH_BIBLE_PASSAGE: str = "Sorry, I couldn't get that Bible passage"
DO_NOT_READ_RESPONSE = "Okay "


def bible_passage_response(passage: str, passage_in_card_text: bool) -> str:
    sent_passage_part: str = " I've sent this bible passage to your Alexa app." if passage_in_card_text else ""
    return f"It's {passage}.{sent_passage_part} Would you like me to read it out? "

# Get next event


def time_to_speech(event_datetime):
    is_evening = event_datetime.hour >= 17
    return f"{event_datetime.hour % 12}:{event_datetime.minute}{(' in the evening' if is_evening else '')}"


def get_next_event(event_name, event_datetime):
    date_string = datetime.strftime(event_datetime, "%A %d %B")
    time_string = time_to_speech(event_datetime)
    return f"The next event is {event_name} on {date_string} at {time_string}. "


NO_EVENTS_FOUND = "There aren't any upcoming events. "

# Get sermon
SERMON_NOT_AVAILABLE = "I'm afraid that sermon isn't available. "


def sermon_preamble(sermon_title, speaker):
    return f"Here's the sermon, {sermon_title}, by {speaker} "
