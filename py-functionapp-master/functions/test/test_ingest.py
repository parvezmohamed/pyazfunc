import unittest
import json
from unittest import mock
import logging

import azure.functions as func

from ingest import ingest

# disable logging while testing
logging.disable(logging.CRITICAL)

class Unit(unittest.TestCase):
        
    def test_empty_body_request(self):
        '''tests that sending an empty body returns 400 response'''
        #setup
        request = func.HttpRequest(
            method='POST',
            url='/api/ingest',
            headers={},
            body=None,
            params={}
        )

        output = mock.MagicMock()
        
        #execute
        response = ingest.main(req=request, msg=output)
        #assert
        self.assertEqual(400, response.status_code)

    def test_validation_for_json(self):
        '''testing that the function validates json'''
        #setup
        body=b'test'

        # dummy request
        request = func.HttpRequest(
            method='POST',
            url='/api/ingest',
            headers={},
            body=body,
            params={}
        )

        # mocking the output binding object
        message = mock.MagicMock()

        #execute
        response = ingest.main(req=request, msg=message)

        #assert
        self.assertEqual(400, response.status_code)

    def test_validation_for_required_fields(self):
        '''testing that the function validates that the body contains the required fields'''
        #setup
        body=b'{"id":"1000"}'

        # dummy request
        request = func.HttpRequest(
            method='POST',
            url='/api/ingest',
            headers={},
            body=body,
            params={}
        )

        # mocking the output binding object
        message = mock.MagicMock()

        #execute
        response = ingest.main(req=request, msg=message)

        #assert
        self.assertEqual(400, response.status_code)

    def test_happy_path(self):
        '''tests that sending a body message is saved to the msg output binding object'''
        #setup
        body = {}
        for required_field in ingest.Constants.REQUIRED_FIELDS:
            body[required_field] = "test_" + required_field
        
        body=json.dumps(body).encode('utf-8')

        # dummy request
        request = func.HttpRequest(
            method='POST',
            url='/api/ingest',
            headers={},
            body=body,
            params={}
        )

        # mocking the output binding object
        message = mock.MagicMock()

        #execute
        response = ingest.main(req=request, msg=message)

        #assert
        self.assertEqual(200, response.status_code)
        message.set.assert_called_once_with(body.decode('utf-8'))


       

        