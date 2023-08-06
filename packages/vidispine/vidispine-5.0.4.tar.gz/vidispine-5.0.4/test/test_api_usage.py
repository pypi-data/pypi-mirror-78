# coding: utf-8
from __future__ import absolute_import

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import unittest

import vidispine
from vidispine.api.access_api import AccessApi  # noqa: E501
from vidispine.rest import ApiException


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.headers['Authorization'] != "Basic YWRtaW46YWRtaW4=":
            self.send_response(401)
            self.end_headers()
            return
        if self.command != "GET":
            self.send_response(404)
            self.end_headers()
            return
        if self.path == "/API/version":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"component":[{"name":"API","version":"5.1"}]}')
        elif self.path == "/API/whoami":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b'admin')
        else:
            self.send_response(404)
            self.end_headers()


class TestApiUsage(unittest.TestCase):
    def setUp(self):
        self.http_thread = HttpThread()
        self.http_thread.start()

        configuration = vidispine.Configuration()
        configuration.host = "http://localhost:6789/API"
        configuration.username = 'admin'
        configuration.password = 'admin'

        self.system_api = vidispine.SystemApi(vidispine.ApiClient(configuration))
        self.user_api = vidispine.UserApi(vidispine.ApiClient(configuration))

    def tearDown(self):
        self.http_thread.terminate()
        self.http_thread.join()

    def testPlainText(self):
        user = self.user_api.get_who_am_i()
        self.assertEqual(user, "admin")

    def testJsonParsing(self):
        api_response = self.system_api.get_version()
        self.assertEqual(api_response.component[0].name, 'API')
        self.assertEqual(api_response.component[0].version, '5.1')


class HttpThread(threading.Thread):
        def run(self):
            self.httpd = HTTPServer(('localhost', 6789), SimpleHTTPRequestHandler)
            self.httpd.serve_forever()

        def terminate(self):
            self.httpd.shutdown()
            self.httpd.server_close()


if __name__ == '__main__':
    unittest.main()
