import config
import requests
import re
from datetime import datetime
from html.parser import HTMLParser


EVENT_NAMES_TO_IGNORE = ["10.15 Service", "6pm Service"]


def strip_html_tags(s):
    return re.sub(r"<.*?>", "", s)


def get_next_event():
    try:
        events = [e
                  for e in requests.get(config.EVENTS_JSON_URL).json()
                  if (e["name"] not in EVENT_NAMES_TO_IGNORE and
                      datetime.strptime(e["datetime_start"], "%Y-%m-%d %H:%M:%S") > datetime.now())]
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    if not events:
        return None

    # Next event, assuming events only includes future events
    events.sort(key=(lambda x: x['datetime_start']))
    event = events[0]

    event_name = event["name"] if event["name"] else ""
    event_description = event["description"] if event["description"] else ""
    event_datetime = (
        datetime.strptime(event["datetime_start"], "%Y-%m-%d %H:%M:%S")
        if event["datetime_start"]
        else None)
    event_location_name = event["location"]["name"] if event["location"]["name"] else ""
    event_small_image_url = (
        event["images"]["original_500"]
        if (event["images"] and event["images"]["original_500"])
        else None)
    event_large_image_url = (
        event["images"]["original_1000"]
        if (event["images"] and event["images"]["original_1000"])
        else None)
    html_unescape = HTMLParser().unescape
    return {
        "name": event_name,
        "datetime": event_datetime,
        "description": strip_html_tags(html_unescape(html_unescape(event_description))),
        "location_name": event_location_name,
        "small_image_url": event_small_image_url,
        "large_image_url": event_large_image_url
    }
