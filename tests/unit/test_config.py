import unittest
import config


class TestConfig(unittest.TestCase):
    def exists_in_config(self, variable_name):
        self.assertTrue(hasattr(config, variable_name))

    def test_amazon_alexa_variables_exist(self):
        self.exists_in_config("APPLICATION_ID")

    def test_bible_api_variables_exist(self):
        self.exists_in_config("BIBLE_TRANSLATION")
        self.exists_in_config("BIBLE_API_URL")

    def test_sermons_variables_exist(self):
        self.exists_in_config("SERMONS_XML_URL")
        self.exists_in_config("SERMONS_XML_NAMESPACE")
        self.exists_in_config("SERMONS_XML_SERVICE_NAMES")
        self.exists_in_config("HTTP_MP3_TO_HTTPS_M3U_API_URL")

    def test_amazon_date_correction_variables_exist(self):
        self.exists_in_config("FUTURE_DAYS_GO_BACK_YEAR_THRESHOLD_SERMONS")
        self.exists_in_config("FUTURE_DAYS_GO_BACK_YEAR_THRESHOLD_PASSAGES")

    def test_ccm_events_variables_exist(self):
        self.exists_in_config("EVENTS_JSON_URL")
