# Alexa skill
APPLICATION_ID = "amzn1.ask.skill.dd677950-cade-4805-b1f1-ce2e3a3569f0"

# Bible API
BIBLE_TRANSLATION = "GNBDC"  # Can't use NIV - it's still in copyright
BIBLE_API_URL = "https://bibles.org/v2/eng-{translation}/passages.js".format(
    translation=BIBLE_TRANSLATION)

# Sermons
SERMONS_XML_URL = "http://www.christchurchmayfair.org/our-talks/podcast/"
SERMONS_XML_NAMESPACE = {
    "ccm": "http://christchurchmayfair.org/",
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"
}
SERMONS_XML_SERVICE_NAMES = {"morning": "Morning Service", "evening": "Evening Service"}
# Alexa audio must be served from https endpoint
HTTP_MP3_TO_HTTPS_M3U_API_URL = ("https://0elu033c2a.execute-api.eu-west-1.amazonaws.com/prod/"
                                 "m3uGenerator")

# Config for correction of AMAZON.Date defaulting to future date if year not given
FUTURE_DAYS_GO_BACK_YEAR_THRESHOLD_SERMONS = 30
FUTURE_DAYS_GO_BACK_YEAR_THRESHOLD_PASSAGES = 150

# CCM Events
EVENTS_JSON_URL = "https://ccmayfair.churchsuite.co.uk/embed/calendar/json"
