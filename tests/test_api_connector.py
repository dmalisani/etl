from unittest import TestCase
from unittest.mock import patch
from data_processor.api_conector import get_category_name
import logging

class MockResponseJson:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestApiLoader(TestCase):

    @patch('data_processor.api_conector.requests.get')
    def test_get_category_name_ok_response(self, request_patch):
        api_response = {
            "name": "tested"
        }
        request_patch.side_effect = (MockResponseJson(api_response, 200),)
        value = get_category_name("my_key")
        self.assertEqual(value, "tested")

    @patch('data_processor.api_conector.requests.get')
    def test_get_category_name_bad_response(self, request_patch):
        api_response = {
            "no_valid_key": "bad_response"
        }
        request_patch.side_effect = (MockResponseJson(api_response, 200),)
        value = get_category_name("my_key")
        self.assertIsNone(value)

    @patch('data_processor.api_conector.requests.get')
    def test_get_category_name_no_connection_to_log(self, request_patch):
        request_patch.side_effect = (ConnectionError,)
        with self.assertLogs("work", level="ERROR"):
            value = get_category_name("my_key")
            self.assertIsNone(value)
