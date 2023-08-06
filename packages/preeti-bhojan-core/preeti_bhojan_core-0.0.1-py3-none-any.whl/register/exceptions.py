"""
Exceptions thrown by register.use_case in addition to util.exceptions
as applicable
"""


class AreaOrLocalityDoesNotExist(Exception):
    """
    Area or locality does not exist
    """


class CustomerAlreadyExists(Exception):
    """
    A customer with a given phone number already exists.
    """


class CuisineDoesNotExist(Exception):
    """
    Cuisine does not exist
    """
