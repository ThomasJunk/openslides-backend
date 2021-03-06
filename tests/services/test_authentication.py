import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any
from unittest import TestCase
from unittest.mock import MagicMock

import pytest  # type: ignore
import simplejson as json

from openslides_backend.main import create_wsgi_application
from openslides_backend.services.authentication import (
    AuthenticationException,
    AuthenticationHTTPAdapter,
)

from ..fake_services.authentication import TestHeaders
from ..utils import Client, ResponseWrapper


class FakeServerRequestHandler(BaseHTTPRequestHandler):
    """
    Request handler for fake server.

    Error can be one of the following strngs: 500, empty, bad.
    """

    def __init__(
        self, user_id: int, error: str = None, *args: Any, **kwargs: Any
    ) -> None:
        self.user_id = user_id
        self.error = error
        super().__init__(*args, **kwargs)

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.end_headers()

    def do_POST(self) -> None:
        if not self.error:
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(str.encode(json.dumps({"user_id": self.user_id})))
        else:
            if self.error == "500":
                self.send_error(500)
            elif self.error == "empty":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
            elif self.error == "bad_missing_key":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(str.encode(json.dumps({})))
            elif self.error == "bad_wrong_key":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    str.encode(json.dumps({"bad_Quuo2Weeph": "bad_Quuo2Weeph"}))
                )


class FakeServerRequestHandlerFactory:
    """
    Factory to generate customized request handlers.
    """

    def __init__(self, user_id: int, error: str = None) -> None:
        self.user_id = user_id
        self.error = error

    def __call__(self, *args: Any, **kwargs: Any) -> FakeServerRequestHandler:
        return FakeServerRequestHandler(self.user_id, self.error, *args, **kwargs)


class FakeServer:
    """
    Simple Python HTTP server for testing purposes.
    """

    # TODO: Make this server faster. It is very slow at the moment.

    def __init__(self, host: str, port: int, user_id: int, error: str = None) -> None:
        self.httpd = HTTPServer(
            (host, port), FakeServerRequestHandlerFactory(user_id, error)
        )
        self.thread = threading.Thread(target=self.httpd.serve_forever)

    def __enter__(self) -> None:
        self.thread.start()

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.httpd.shutdown()


@pytest.mark.skipif(
    not os.environ.get("OPENSLIDES_BACKEND_RUN_ALL_TESTS"), reason="Test is very slow."
)
class AuthenticationHTTPAdapterTester(TestCase):
    def setUp(self) -> None:
        self.host = "localhost"
        self.port = 9000
        self.auth = AuthenticationHTTPAdapter(
            # TODO: Use a function from environment.py. Don't declare host and port twice.
            authentication_url=f"http://{self.host}:{self.port}",
            logging=MagicMock(),
        )

    def test_get_anonymous(self) -> None:
        with FakeServer(self.host, self.port, 0):
            headers = TestHeaders()
            user_id = self.auth.get_user(headers)
            self.assertEqual(user_id, 0)

    def test_some_user(self) -> None:
        expected_user_id = 5262746456
        with FakeServer(self.host, self.port, expected_user_id):
            headers = TestHeaders()
            user_id = self.auth.get_user(headers)
            self.assertEqual(user_id, expected_user_id)

    def test_http_500(self) -> None:
        with FakeServer(self.host, self.port, 3238429704, "500"):
            headers = TestHeaders()
            with self.assertRaises(AuthenticationException) as context_manager:
                self.auth.get_user(headers)
            self.assertEqual(
                context_manager.exception.message,
                "Authentication service sends HTTP 500.",
            )

    def test_empty_payload(self) -> None:
        with FakeServer(self.host, self.port, 2896946348, "empty"):
            headers = TestHeaders()
            with self.assertRaises(AuthenticationException) as context_manager:
                self.auth.get_user(headers)
            self.assertEqual(
                context_manager.exception.message,
                "Bad response from authentication service. Body does not contain JSON.",
            )

    def test_bad_payload_1(self) -> None:
        with FakeServer(self.host, self.port, 9198030928, "bad_missing_key"):
            headers = TestHeaders()
            with self.assertRaises(AuthenticationException) as context_manager:
                self.auth.get_user(headers)
            self.assertEqual(
                context_manager.exception.message,
                "Empty or bad response from authentication service.",
            )

    def test_bad_payload_2(self) -> None:
        with FakeServer(self.host, self.port, 4765864300, "bad_wrong_key"):
            headers = TestHeaders()
            with self.assertRaises(AuthenticationException) as context_manager:
                self.auth.get_user(headers)
            self.assertEqual(
                context_manager.exception.message,
                "Empty or bad response from authentication service.",
            )

    def test_wsgi_request_missing_body(self) -> None:
        # This this does not touch the fake auth server.
        with FakeServer(self.host, self.port, 6052759165):
            client = Client(create_wsgi_application("ActionsView"), ResponseWrapper)
            response = client.post(
                "/system/api/actions", content_type="application/json"
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn("Failed to decode JSON object", str(response.data))

    def test_wsgi_request_error(self) -> None:
        with FakeServer(self.host, self.port, 7824698278, "500"):
            client = Client(create_wsgi_application("ActionsView"), ResponseWrapper)
            response = client.post("/system/api/actions", json=[])
            self.assertEqual(response.status_code, 400)
            self.assertIn("Authentication service sends HTTP 500.", str(response.data))
