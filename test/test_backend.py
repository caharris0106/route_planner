import sys
sys.path.append("../")
import unittest
from backend import app, db, User
from flask import Flask
# from urllib.resposx`
from flask_testing import TestCase

# class TestBackend(unittest.TestCase):
#
#     def test_add(self):
#         result = backend.add(10, 4)
#         self.assertEqual(result, 14)


class MyTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_greeting(self):
        response = self.client.get('/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    MyTest().test_greeting()
