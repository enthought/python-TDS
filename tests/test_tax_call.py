from unittest import TestCase
import mock

from TDS.tax import TaxAPI
from TDS.exceptions import TDSResponseError


class TestTDSTaxCalls(TestCase):

    def test_calling_convention(self):
        # GIVEN
        login_id = 'login_id'
        password = 'password'
        tax_api = TaxAPI(login_id, password)
        tax_api._client = client = mock.Mock()

        # WHEN
        try:
            tax_api._make_call('SomeTDSMethod')
        except TDSResponseError:
            pass

        # THEN
        self.assertEqual(
            client.service.SomeTDSMethod.call_args,
            mock.call(username=login_id, password=password)
        )

    def test_successful_method_call(self):
        # GIVEN
        tax_api = TaxAPI('login_id', 'password')
        tax_api._client = client = mock.Mock()
        client.service.SomeTDSMethod.return_value = response = mock.Mock()
        response.ServiceStatus.StatusNo = 101

        # WHEN
        actual_response = tax_api._make_call('SomeTDSMethod')

        # THEN
        self.assertEqual(actual_response, response)

    def test_unsuccessful_method_call(self):
        # GIVEN
        tax_api = TaxAPI('login_id', 'password')
        tax_api._client = client = mock.Mock()
        client.service.SomeTDSMethod.return_value = response = mock.Mock()
        response.ServiceStatus.StatusNo = 400
        response.ServiceStatus.StatusDescription = desc = 'error description'

        # WHEN
        with self.assertRaises(TDSResponseError) as ctx:
            tax_api._make_call('SomeTDSMethod')

        # THEN
        exc = ctx.exception
        data = exc.full_response
        self.assertEqual(data['response_code'], 400)
        self.assertEqual(data['response_text'], desc)

    def test_get_tax_data(self):
        # GIVEN
        tax_api = TaxAPI('login_id', 'password')
        tax_api._client = client = mock.Mock()
        client.service.GetUSAddressVerificationTaxPlainNetwork.return_value = \
            response = mock.Mock()
        response.ServiceStatus.StatusNo = 101

        address1 = 'address line 1'
        address2 = 'address line 2'
        citystatezip = 'City, State, Zip'

        # WHEN
        _, tax = tax_api.get_tax_data(address1, citystatezip, address2)

        # THEN
        expected = [
            'city_sales_tax', 'mta_sales_tax', 'county_sales_tax',
            'state_sales_tax', 'total_sales_tax', 'city_reporting_code',
            'county_reporting_code'
        ]
        self.assertItemsEqual(tax.keys(), expected)

    def test_get_remaining_hits(self):
        # GIVEN
        tax_api = TaxAPI('login_id', 'password')
        tax_api._client = client = mock.Mock()
        client.service.GetRemainingHitsPlainNetwork.return_value = hits = 123

        # WHEN
        response = tax_api.get_remaining_hits()

        # THEN
        self.assertEqual(response, hits)
