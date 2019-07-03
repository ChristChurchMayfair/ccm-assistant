from datetime import datetime


# Welcome
WELCOME_TITLE = "Christ Church Mayfair"
WELCOME_CONTENT = "Hello! Ask me for the bible reading for a service or a past sermon."

# End session
END_SESSION_TITLE = "See you later!"
END_SESSION_CONTENT = "Thanks for using Christ Church Mayfair Assistant!"

# Get passage
GET_PASSAGE_TITLE = "Bible reading for {date} {service} service"


def format_get_passage_content(passage_text: str, passage: str, bible_translation: str) -> str:
    return f"{passage_text}\n{passage} ({bible_translation})"


def get_passage_title(date, service):
    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        day_suffix = "th"
    else:
        day_suffix = ["st", "nd", "rd"][date.day % 10 - 1]

    date_text: str = f"{str(date.day)}{day_suffix} {date.strftime('%B %Y')}"
    service_text = "AM" if service == "morning" else "PM"
    return GET_PASSAGE_TITLE.format(date=date_text, service=service_text)


def get_sermon_content(passage, series_name, speaker):
    return f"{passage}\n{series_name}\n{speaker}"


def get_next_event_title(event_title, event_datetime):
    date_string: str = datetime.strftime(event_datetime, "%A %d %B")
    time_string: str = datetime.strftime(event_datetime, "%H:%M")
    return f"{event_title} - {time_string}, {date_string}"


def get_next_event_content(event_description, event_location_name):
    return (
        f"{event_description}\nLocation: {event_location_name}"
        if event_description
        else event_location_name)
