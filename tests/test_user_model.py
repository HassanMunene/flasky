import unittest
from app.models import User
"""
This module will be used the different aspects
of the User model
"""


class UserModelTestCase(unittest.TestCase):

    def test_password_setter(self):
        u1 = User(password = 'Hassan')
        self.assertTrue(u1.password_hash is not None)

    def test_no_password_getter(self):
        u1 = User(password = 'Hassan')
        with self.assertRaises(AttributeError):
            u1.password

    def test_password_verification(self):
        u1 = User(password = 'Hassan')
        self.assertTrue(u1.verify_password('Hassan'))
        self.assertFalse(u1.verify_password('Munene'))

    def test_password_salts_are_random(self):
        u1 = User(password = 'Hassan')
        u2 = User(password = 'Hassan')
        self.assertTrue(u1.password_hash != u2.password_hash)
