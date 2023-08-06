class AuthenticationError(Exception):
    """Raised when login credentials are missing"""

    message = """
    Autenthication failed.
    The required configuration setting {} was not found in your environment.
    To authenticate follow the instructions explained in the README:
    https://gitlab.com/coopdevs/pymasmovil#login
    """

    def __init__(self, missing_credential):
        self.message = self.message.format(missing_credential)
        super(AuthenticationError, self).__init__(self.message)


class AccountRequiredParamsError(Exception):
    """Raised when trying to create an account without some required paramether"""

    message = """
    .
    Missing required paramether "{}" to create an account.
    Please make sure all required parameters are provided:
    [corporateName*, documentNumber, documentType, nationality*, email,
    name*, surname*, phone, postalCode, province, region, roadName,
    roadNumber, roadType, town]
    * if appropriate, according to documentType
    """

    def __init__(self, missing_paramether):
        self.message = self.message.format(missing_paramether)
        super().__init__(self.message)


class UnknownMMError(Exception):
    """Raised when the MM API returns an error with an unknown structure"""

    def __init__(self, MM_response_body):
        self.message = MM_response_body
        super().__init__(self.message)
