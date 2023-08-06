class AuthenticationError(Exception):
    """
    Returned when -
    1. Phone number is invalid or a customer with the phone number does not exist
    2. Phone number, password combination is invalid
    """
    pass


class InvalidInput(Exception):
    """
    Returned when -
    1. Request is not json
    2. A required field is null or empty
    """
    pass


class NotScheduled(Exception):
    """
    The operation to be performed required the customer to schedule first.
    """
    pass
