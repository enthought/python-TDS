"""
Debug responses for the TDS Client.

"""


class _DebugResponse(object):
    class ServiceResult(object):
        StatusNo = 101

DEBUG_HITS = 255
DEBUG_TAX = {
    "city_sales_tax": 0.01,
    "mta_sales_tax": 0.02,
    "county_sales_tax": 0.04,
    "state_sales_tax": 0.08,
    "total_sales_tax": 0.15
}

DEBUG_RESPONSE = _DebugResponse()
