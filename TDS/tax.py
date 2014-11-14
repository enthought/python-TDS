from suds import WebFault
from suds.client import Client

from TDS.exceptions import TDSConnectionError, TDSResponseError

from .debug import DEBUG_HITS, DEBUG_RESPONSE, DEBUG_TAX

WSDL = 'http://service.taxdatasystems.net/USAddressVerification.svc?WSDL'
LOCATION = 'http://service.taxdatasystems.net/USAddressVerification.svc/basic'


class TaxAPI(object):

    debug_remaining_hits = DEBUG_HITS

    debug_tax_data = (DEBUG_RESPONSE, DEBUG_TAX)

    def __init__(self, login_id, password, debug=False):
        self.url = WSDL
        self.location = LOCATION
        self.login_id = login_id
        self.password = password
        self.debug = debug

    @property
    def client(self):
        if not hasattr(self, '_client'):
            self._client = Client(self.url, location=self.location)
        return self._client

    def _make_call(self, service, *args):
        method = getattr(self.client.service, service)
        try:
            response = method(username=self.login_id,
                              password=self.password, *args)
        except WebFault as e:
            raise TDSConnectionError("Error contacting SOAP API")
        status = response.ServiceStatus
        if status.StatusNo != 101:
            error_code = status.StatusNo
            error_text = status.StatusDescription
            e = TDSResponseError("%s: %s" % (error_code, error_text))
            e.full_response = {
                'response_code': error_code,
                'response_text': error_text,
                }
            raise e
        return response

    def get_tax_data(self, address1, citystatezip, address2=None):
        if self.debug:
            return self.debug_tax_data

        response = self._make_call("GetUSAddressVerificationTaxPlainNetwork",
                                   address1, address2, citystatezip)
        tax = {
            "city_sales_tax": response.ServiceResult.CitySalesTax,
            "mta_sales_tax": response.ServiceResult.MTASalesTax,
            "county_sales_tax": response.ServiceResult.CountySalesTax,
            "state_sales_tax": response.ServiceResult.StateSalesTax,
            "total_sales_tax": response.ServiceResult.TotalSalesTax,
        }
        return response, tax

    def get_remaining_hits(self):
        if self.debug:
            return self.debug_remaining_hits

        method = getattr(self.client.service, "GetRemainingHitsPlainNetwork")
        response = method(username=self.login_id, password=self.password)
        return response
