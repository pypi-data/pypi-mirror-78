"""
Models for register i.e. customer, home address and office address.
These are plain data structures and just know if the data they are
holding makes sense.
"""

from email_validator import validate_email, EmailNotValidError

from util.exceptions import InvalidInput
from util.string import is_alphanumeric_underscore_or_space


# Default arguments are added to allow positional arguments


class Customer:
    """
    Represents a customer.
    """

    first_name: str
    last_name: str
    email: str
    phone_number: str
    password: str

    def __init__(self, first_name='', last_name='', email='', phone_number='', password=''):

        if first_name is None or \
                last_name is None or \
                email is None or \
                phone_number is None or \
                password is None:
            raise InvalidInput

        self.first_name = first_name
        self.last_name = last_name
        self.email = ''

        try:
            # By default validate_email checks if email can be delivered
            # i.e. it makes a network request. This is disables because -
            #
            # 1. We do not need this level of authenticity because we are
            # taking all payments before hand
            # 2. It slows down testing by orders of magnitudes.

            self.email = validate_email(email.strip(), check_deliverability=False).email
            self.is_valid_email = True
        except EmailNotValidError:
            self.is_valid_email = False

        self.phone_number = phone_number
        self.password = password.strip()

    def is_first_name_valid(self):
        return self.first_name.isalpha()

    def is_last_name_valid(self):
        return self.last_name.isalpha()

    def is_email_valid(self):
        return self.is_valid_email

    def is_phone_number_valid(self):
        try:
            return len(self.phone_number) == 10 and int(self.phone_number) > 0
        except ValueError:
            # ValueError is thrown by int() when phone number is not a valid integer.
            # If that's the case, phone number is invalid
            return False

    def is_password_valid(self):
        return 8 <= len(self.password.strip()) <= 70

    def is_valid(self):

        return self.is_first_name_valid() and \
               self.is_last_name_valid() and \
               self.is_email_valid() and \
               self.is_phone_number_valid() and \
               self.is_password_valid()

    @staticmethod
    def from_json(json):
        return Customer(
            json['first_name'],
            json['last_name'],
            json['email'],
            json['phone_number'],
            json['password']
        )


# If you change Home address, remember to change change_home_address


class HomeAddress:
    """
    Represents home address of customer
    """

    society: str
    building: str
    flat_number: str
    locality_id: int

    def __init__(self, flat_number='', building='', society='', locality_id=-1):
        if flat_number is None or building is None or society is None or locality_id is None:
            raise InvalidInput

        self.society = society.strip()
        self.building = building.strip()
        self.flat_number = flat_number.strip()
        # Locality id is given by the server to the client and
        # it is checked against database. So there is no need to neither
        # strip nor validate
        self.locality_id = locality_id

    def is_society_valid(self):
        return is_alphanumeric_underscore_or_space(self.society)

    def is_building_valid(self):
        return is_alphanumeric_underscore_or_space(self.building)

    def is_flat_number_valid(self):
        return is_alphanumeric_underscore_or_space(self.flat_number)

    def is_locality_valid(self):
        return self.locality_id >= 0

    def is_valid(self):
        return self.is_society_valid() and \
               self.is_building_valid() and \
               self.is_locality_valid() and \
               self.is_flat_number_valid()

    @staticmethod
    def from_json(json):
        return HomeAddress(
            json['flat_number'],
            json['building'],
            json['society'],
            json['locality_id']
        )


# If you change office address, remember to change change_office_address


class OfficeAddress:
    """
    Represents office address of customer
    """
    office_number: str
    floor: int
    tower: str
    area_id: int
    company: str

    def __init__(self, office_number='', floor=0, tower='', area_id=-1, company=''):
        if office_number is None or \
                floor is None or \
                tower is None or \
                area_id is None or \
                company is None:
            raise InvalidInput

        self.floor = floor
        self.tower = tower.strip()
        self.office_number = office_number.strip()
        self.area_id = area_id
        self.company = company

    def is_office_number_valid(self):
        return is_alphanumeric_underscore_or_space(self.office_number)

    def is_floor_valid(self):
        return self.floor >= 0

    def is_tower_valid(self):
        return is_alphanumeric_underscore_or_space(self.tower)

    def is_area_valid(self):
        return self.area_id >= 0

    def is_company_valid(self):
        return is_alphanumeric_underscore_or_space(self.company)

    def is_valid(self):
        return self.is_office_number_valid() and \
               self.is_floor_valid() and \
               self.is_tower_valid() and \
               self.is_area_valid() and \
               self.is_company_valid()

    @staticmethod
    def from_json(json):
        return OfficeAddress(
            json['office_number'],
            json['floor'],
            json['tower'],
            json['area_id'],
            json['company']
        )
