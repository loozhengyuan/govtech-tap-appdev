from django.test import TestCase


# TODO: Remove TemporaryTestCase
class TemporaryTestCase(TestCase):
    """Temporarily allow pytest to exit without errors when there are no tests"""
    def test_is_temporary(self):
        self.assertTrue
