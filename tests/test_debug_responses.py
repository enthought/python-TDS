import unittest

from TDS.tax import TaxAPI
from TDS.debug import DEBUG_HITS, DEBUG_RESPONSE, DEBUG_TAX


class TestDebugResponses(unittest.TestCase):

    def test_debug_defaults(self):
        # Check that we get the debug values when debugging mode is enabled.
        client = TaxAPI('dummy_user', 'password', debug=True)
        self.assertEqual(client.get_remaining_hits(), DEBUG_HITS)
        response, tax = client.get_tax_data('address1', 'address2')
        self.assertEqual(response, DEBUG_RESPONSE)
        self.assertEqual(tax, DEBUG_TAX)


if __name__ == '__main__':
    unittest.main()
