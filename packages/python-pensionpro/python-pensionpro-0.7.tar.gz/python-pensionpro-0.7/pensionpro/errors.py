from requests import HTTPError

class PensionProError(HTTPError):
    """ Base Error Class """

class PensionProBadRequest(PensionProError):
    """ Most 40X and 501 errors """

class PensionProUnauthorized(PensionProError):
    """ 401 Unauthorized """

class PensionProAccessDenied(PensionProError):
    """ 404 Unauthorized """

class PensionProRateLimited(PensionProError):
    """ 429 Rate Limit Reached """

class PensionProNotFound(PensionProError):
    """ 404 Not Found """

class PensionProServerError(PensionProError):
    """ 50X Errors """
