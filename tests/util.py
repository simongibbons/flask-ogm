from unittest import TestCase
from flask import Flask


class FlaskOGMTestCase(TestCase):
    def create_test_app(self, **kwargs):
        app = Flask('test_app')
        app.testing = True
        client = app.test_client()
        app.config.update(**kwargs)
        return app, client
