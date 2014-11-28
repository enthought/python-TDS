from unittest import TestCase

from TDS.utils import convert


class TestUtils(TestCase):

    def test_convert(self):
        self.assertEqual(convert('CamelCase'), 'camel_case')
        self.assertEqual(convert('HTTPError'), 'http_error')
