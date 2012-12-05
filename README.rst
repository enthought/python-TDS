Python-TDS
==========

A Python wrapper around the TaxDataSystems Sales Tax API.

::

    >>> # Init the client
    >>> from TDS.tax import TaxAPI
    >>> client = TaxAPI("login_id", "password")
    
    >>> # Get sales tax for a given address
    >>> response, tax = cliet.get_tax_data(address1="", citystatezip="")
    
    >>> # Get remaining hits
    >>> hits = client.get_remaining_hits()


