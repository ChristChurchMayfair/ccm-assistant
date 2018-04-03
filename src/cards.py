# Welcome
WELCOME_TITLE = "Christ Church Mayfair Assistant"
WELCOME_CONTENT = "Welcome! Ask me for the bible reading for a service or a past sermon."

# End session
END_SESSION_TITLE = "See you later!"
END_SESSION_CONTENT = "Thanks for using Christ Church Mayfair Assistant!"

# Get passage
GET_PASSAGE_TITLE = "Bible reading for {date} {service} service"
GET_PASSAGE_CONTENT = u"{passage_text}\n{passage} ({bible_translation})"


def get_passage_title(date, service):
    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        day_suffix = "th"
    else:
        day_suffix = ["st", "nd", "rd"][date.day % 10 - 1]

    date_text = "{day}{day_suffix} {month_year}".format(day=str(date.day), day_suffix=day_suffix,
                                                        month_year=date.strftime("%B %Y"))
    service_text = "AM" if service == "morning" else "PM"
    return GET_PASSAGE_TITLE.format(date=date_text, service=service_text)


# Get sermon
GET_SERMON_TITLE = "{sermon_title}"
GET_SERMON_CONTENT = "{passage}\n{series_name}\n{speaker}"
