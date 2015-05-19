Python-TDS
==========

A Python wrapper around the `Address Validation & Zip+4 Tax Rates Web Service`_
from `TaxDataSystems`_.

.. code:: python

    >>> # Init the client
    >>> from TDS.tax import TaxAPI
    >>> client = TaxAPI("login_id", "password")

    >>> # Get sales tax for a given address
    >>> response, tax = client.get_tax_data(address1="", citystatezip="")

    >>> # Get remaining hits
    >>> hits = client.get_remaining_hits()


.. _`Address Validation & Zip+4 Tax Rates Web Service`: https://www.taxdatasystems.net/Down/Address%20Validation%20zip4%20Edition%20Web%20Service%20Documentation.pdf

.. _TaxDataSystems: https://www.taxdatasystems.net/
