# This module provides a unittest subclass with helper methods for conducting API tests.
#
# Logging should be turned on.

import logging
import unittest
from enum import Enum
from json import JSONDecodeError

import requests


def json_path_to_str(path):
    if isinstance(path, list):
        return '.'.join(path)
    elif path is None:
        return ''
    return path


# Utilities for writing tests

class HttpMethod(Enum):
    POST = 1
    GET = 2
    DELETE = 3


class ApiTest(unittest.TestCase):
    """Provides helper methods for an API test formed like a unit test."""

    @staticmethod
    def health_check_or_die(url=None):
        if url is None:
            raise Exception('Parameter [url] was not given but is required.')

        # noinspection PyBroadException
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise Exception('Failed to connect to ' + url + '. Is the server running?')
        except requests.exceptions.Timeout:
            raise Exception('Timed out while attempting to connect to ' + url + '. Is the server running?')
        except Exception:
            pass
        logging.info('Health check passed.')

    # noinspection PyMethodMayBeStatic
    def send_request(self, url, http_method=None, headers=None):
        if http_method is None:
            http_method = HttpMethod.GET

        logging.debug('Sending ' + http_method.name + " request to " + url)
        if http_method == HttpMethod.GET:
            resp = requests.get(url, headers=headers)
        else:
            raise Exception('Unimplemented REST method.')

        try:
            body = resp.json()
        except JSONDecodeError:
            body = ''

        logging.debug('Response: HTTP/1.1 ' + str(resp.status_code) + ' ' + str(body))
        return resp

    def assert_resp_code(self, resp, expected_status_code):
        """Passes if the response code is the expected value.

        :param resp: Response body from an HTTP request.
        :param expected_status_code: Type requests.codes -- Expected HTTP status code value.
        """

        self.assertEqual(resp.status_code,
                         expected_status_code,
                         'Incorrect HTTP response code. Expected ' +
                         str(expected_status_code) + ', received ' + str(resp.status_code) + '.')

    def get_resp_body(self, response):
        self.assertTrue(response.json(), 'There is no response body but a response body was expected.')
        return response.json()

    def get_resp_body_value(self, resp, path_to_value=None):
        """Passes if the response body has the value in the given path.

        :param resp: HTTP response object.
        :param path_to_value: If string, single key to the value. If list, keys to iterate through to reach value.
        :return: Corresponding value in the JSON body.
        """
        if path_to_value is None:
            return self.get_resp_body(resp)

        body = resp.json()
        failure_message = 'Key ' + \
                          json_path_to_str(path_to_value) + \
                          ' is required but was not found in the response body.'

        try:
            if path_to_value is None:
                value = body
            elif isinstance(path_to_value, list):
                value = body
                for key in path_to_value:
                    value = value[key]
            else:
                value = body[path_to_value]
        except KeyError:
            self.fail(failure_message)

        self.assertTrue(value, failure_message)
        return value

    def get_resp_body_str(self, resp, path_to_value=None):
        value = self.get_resp_body_value(resp, path_to_value)
        self.assertTrue(isinstance(value, str),
                        'Value ' + json_path_to_str(path_to_value) + ':' + str(
                            value) + ' was expected to be a string.')
        return value

    def get_resp_body_num(self, resp, path_to_value=None):
        value = self.get_resp_body_value(resp, path_to_value)
        self.assertTrue(isinstance(value, int),
                        'Value ' + json_path_to_str(path_to_value) + ':' + str(value) + ' was expected to be a int.')
        return value

    def get_resp_body_list(self, resp, path_to_value=None):
        value = self.get_resp_body_value(resp, path_to_value)
        self.assertTrue(isinstance(value, list),
                        'Value ' + json_path_to_str(path_to_value) + ':' + str(value) + ' was expected to be a list.')
        return value
