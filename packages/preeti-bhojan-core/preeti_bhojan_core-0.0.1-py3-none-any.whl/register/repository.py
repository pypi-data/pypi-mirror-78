"""
The interface the use case expects the repository to implement
"""

import abc


class RegisterRepository(abc.ABC):
    """
    Repository required by register
    """

    @abc.abstractmethod
    def locality_exists(self, locality_id):
        """
        Check if the given locality id exists in the database
        :param locality_id: the locality id to check
        :return: True if locality id exists; false otherwise
        """

    @abc.abstractmethod
    def area_exists(self, area_id):
        """
        Check if the given area id exists in the database
        :param area_id: the area id to check
        :return: True if area id exists; false otherwise
        """

    @abc.abstractmethod
    def cuisine_exists(self, cuisine_id):
        """
        Check if the given cuisine id exists in the database
        :param cuisine_id: the cuisine id to check
        :return: True if cuisine id exists; false otherwise
        """

    @abc.abstractmethod
    def customer_exists(self, phone_number):
        """
        Check if customer with the phone number already exists.
        :param phone_number: Phone number to check
        :return: Returns True if customer exists; false otherwise.
        """

    @abc.abstractmethod
    def insert(self, customer, home_address, office_address, cuisine_id):
        """
        Insert the given customer with their home address, office
        address and cuisine id. Either home address or office address
        might be None but at least one of them should be provided.

        If both are None, the behaviour is undefined but will probably
        raise some exception
        :param customer: customer to insert
        :param home_address: home address of customer (conditionally nullable)
        :param office_address: office address of customer (conditionally nullable)
        :param cuisine_id: cuisine id of the customer.
        :return: Nothing
        """
