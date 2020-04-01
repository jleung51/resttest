#!/usr/bin/env python3

from resttest import ApiTest

import logging
import unittest
import requests

SERVER_URL = "http://localhost:8080"

URLS = dict(
    HEALTH_CHECK=SERVER_URL,
    ABOUT=SERVER_URL + '/api/about',
    DUMP_MODEL=SERVER_URL + '/api/dump-model',
    DEPARTMENTS=SERVER_URL + '/api/departments'
)


class AboutApis(ApiTest):
    url = URLS['ABOUT']
    headers = {'Content-Type': 'application/json'}

    def test_get(self):
        resp = self.send_request(self.url, headers=self.headers)
        self.assert_resp_code(resp, requests.codes.ok)
        self.get_resp_body_str(resp, 'appName')
        self.get_resp_body_str(resp, 'authorName')


class DumpModelApis(ApiTest):
    url = URLS['DUMP_MODEL']
    headers = {'Content-Type': 'application/json'}

    def test_get(self):
        resp = self.send_request(self.url, headers=self.headers)
        self.assert_resp_code(resp, requests.codes.ok)


class DepartmentApis(ApiTest):
    url = URLS['DEPARTMENTS']
    headers = {'Content-Type': 'application/json'}

    # Valid values from reading course_data_2018.csv
    dept_id = 2  # CMPT
    course_id = 8  # 213
    offering_id = 0

    @staticmethod
    def generate_url(dept_id=None, course_id=None, offering_id=None):
        url = DepartmentApis.url

        if dept_id is not None:
            url += '/' + str(dept_id) + '/courses'
            if course_id is not None:
                url += '/' + str(course_id) + '/offerings'
                if offering_id is not None:
                    url += '/' + str(offering_id)

        return url

    def test_get_departments(self):

        # Given
        url = DepartmentApis.generate_url()

        # When
        resp = self.send_request(url, headers=self.headers)

        # Then
        self.assert_resp_code(resp, requests.codes.OK)
        departments = self.get_resp_body_list(resp)
        self.assertTrue(len(departments), 'Response body is empty, but must contain a list of departments.')
        self.assertTrue(departments[2], 'Response body should have more departments.')

    def test_get_courses_of_dept(self):

        # Given
        url = DepartmentApis.generate_url(self.dept_id)

        # When
        resp = self.send_request(url, headers=self.headers)

        # Then
        self.assert_resp_code(resp, requests.codes.OK)
        courses = self.get_resp_body_list(resp)
        self.assertTrue(len(courses), 'Response body is empty, but must contain a list of courses.')
        self.assertTrue(courses[2], 'Response body should have more courses.')

    def test_get_sections_of_course(self):

        # Given
        url = DepartmentApis.generate_url(self.dept_id, self.course_id)

        # When
        resp = self.send_request(url, headers=self.headers)

        # Then
        self.assert_resp_code(resp, requests.codes.OK)
        sections = self.get_resp_body_list(resp)
        self.assertTrue(len(sections), 'Response body is empty, but must contain a list of sections.')
        self.assertTrue(sections[1], 'Response body should have more sections.')

    def test_get_offering(self):

        # Given
        url = DepartmentApis.generate_url(self.dept_id, self.course_id, self.offering_id)

        # When
        resp = self.send_request(url, headers=self.headers)

        # Then
        self.assert_resp_code(resp, requests.codes.OK)
        offerings = self.get_resp_body_list(resp)
        self.assertTrue(len(offerings), 'Response body is empty, but must contain a list of offerings.')
        self.assertTrue(offerings[0], 'Response body should have more offerings.')

    def test_invalid_department(self):

        # Given
        url = DepartmentApis.generate_url(99999)

        # When
        resp = self.send_request(url, headers=self.headers)

        # Then
        self.assert_resp_code(resp, requests.codes.NOT_FOUND)

    def test_invalid_department_course_search(self):

        # Given
        url = DepartmentApis.generate_url(
            99999,
            self.course_id)

        # When
        resp = self.send_request(url, headers=self.headers)

        # Then
        self.assert_resp_code(resp, requests.codes.NOT_FOUND)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)

    ApiTest.health_check_or_die(URLS['HEALTH_CHECK'])
    unittest.main()
