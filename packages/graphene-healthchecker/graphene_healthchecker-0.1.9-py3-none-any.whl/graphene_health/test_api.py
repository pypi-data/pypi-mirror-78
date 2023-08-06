# -*- coding: utf-8 -*-
from flask_testing import TestCase
from .views import app


class Testcases(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
        return app

    def test_healthendpoint(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/-/health").status_code, 200)
