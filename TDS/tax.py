import functools
import re

from suds import WebFault
from suds.client import Client

from TDS.exceptions import TDSConnectionError, TDSResponseError

from .utils import convert

WSDL = 'http://service.taxdatasystems.net/USAddressVerification.svc?WSDL'
LOCATION = 'http://service.taxdatasystems.net/USAddressVerification.svc/basic'


def remove_hashtags(f):
    """Remove hashtags from string arguments of wrapped function.

    For some reason, getting the tax info for an address that contains
    hash signs (e.g. "apartment #5") will cause TDS to fail with a 500
    internal server error (see GitHub issue #2 for more details). This
    decorator ensures that any hash signs in the function's arguments
    are replaced by a reasonable alternative.

    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        def _replace_hashtag(arg):
            if isinstance(arg, basestring):
                return re.sub('#\s?', 'no. ', arg)
            else:
                return arg
        args = [_replace_hashtag(arg) for arg in args]
        return f(*args, **kwargs)
    return wrapper


class TaxAPI(object):

    # A list of SOAP attributes on the TDS response that will be exposed on the
    # Python side.
    exposed_tax_fields = [
        'CitySalesTax',
        'MTASalesTax',
        'CountySalesTax',
        'StateSalesTax',
        'TotalSalesTax',
        'CityReportingCode',
        'CountyReportingCode'
    ]

    def __init__(self, login_id, password):
        self.url = WSDL
        self.location = LOCATION
        self.login_id = login_id
        self.password = password

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

    @remove_hashtags
    def get_tax_data(self, address1, citystatezip, address2=None):
        """Retrieve tax information for a given address.

        Parameters
        ----------
        address1: str
            First address line
        citystatezip: str
            City, state and zip as a space-separated string.
        address2: str
            Second line of the address (if any).

        Returns
        -------
        response: object
            Raw SOAP response
        tax: dict
            Tax rates on city and state level.

        """
        response = self._make_call("GetUSAddressVerificationTaxPlainNetwork",
                                   address1, address2, citystatezip)

        tax = {
            convert(field): getattr(response.ServiceResult, field)
            for field in self.exposed_tax_fields
        }
        return response, tax

    def get_remaining_hits(self):
        """Retrieve remaining hits against TDS.

        Returns
        -------
        hits: int
            Number of available hits remaining.

        """
        method = getattr(self.client.service, "GetRemainingHitsPlainNetwork")
        response = method(username=self.login_id, password=self.password)
        return response
