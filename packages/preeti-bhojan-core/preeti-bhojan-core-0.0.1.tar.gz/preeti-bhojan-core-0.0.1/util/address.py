from get_home_address.repository import get_home_address
from get_office_address.repository import get_office_address


class AddressRepository:
    def has_home_address(self, phone_number):
        return 'enabled' not in get_home_address(phone_number)

    def has_office_address(self, phone_number):
        return 'enabled' not in get_office_address(phone_number)