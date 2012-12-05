class TDSError(Exception):
    """Base class for all errors."""

class TDSConnectionError(TDSError):
    """Error communicating with the Authorize.net API."""

class TDSResponseError(TDSError):
    """Error response code returned from API."""

class TDSInvalidError(TDSError):
    """Invalid information provided."""