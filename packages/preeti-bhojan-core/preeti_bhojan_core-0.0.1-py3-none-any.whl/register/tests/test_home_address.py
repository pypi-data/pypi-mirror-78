import unittest

from register.models import HomeAddress, InvalidInput
from register.tests.input import alphaNumericWithSpacesAndUnderscore


class JsonTest(unittest.TestCase):
    def test_from_json(self):
        home_address = HomeAddress.from_json({
            'flat_number': 'abc',
            'building': 'def',
            'society': 'ghi',
            'locality_id': 1
        })

        self.assertEqual(home_address.flat_number, 'abc')
        self.assertEqual(home_address.building, 'def')
        self.assertEqual(home_address.society, 'ghi')
        self.assertEqual(home_address.locality_id, 1)


class NoneTest(unittest.TestCase):
    def test_constructor_throws_invalid_input_when_flat_number_is_none(self):
        with self.assertRaises(InvalidInput):
            HomeAddress(None, '', '', 0)

    def test_constructor_throws_invalid_input_when_building_is_none(self):
        with self.assertRaises(InvalidInput):
            HomeAddress('', None, '', 0)

    def test_constructor_throws_invalid_input_when_society_is_none(self):
        with self.assertRaises(InvalidInput):
            HomeAddress('', '', None, 0)

    def test_constructor_throws_invalid_input_when_locality_id_is_none(self):
        with self.assertRaises(InvalidInput):
            HomeAddress('', '', '', None)


class IndividualFieldsTest(unittest.TestCase):
    def test_society_should_contain_alphabets_numbers_underscore_and_space(self):
        for society, isValid in alphaNumericWithSpacesAndUnderscore.items():
            home_address = HomeAddress(society=society)
            self.assertEqual(home_address.is_society_valid(), isValid)

    def test_building_should_contain_alphabets_numbers_underscore_and_space(self):
        for building, isValid in alphaNumericWithSpacesAndUnderscore.items():
            home_address = HomeAddress(building=building)
            self.assertEqual(home_address.is_building_valid(), isValid)

    def test_flat_number_should_contain_alphabets_numbers_underscore_and_space(self):
        for flat_number, isValid in alphaNumericWithSpacesAndUnderscore.items():
            home_address = HomeAddress(flat_number=flat_number)
            self.assertEqual(home_address.is_flat_number_valid(), isValid)

    def test_locality_is_not_negative(self):
        home_address = HomeAddress()
        self.assertFalse(home_address.is_locality_valid())

        home_address.locality_id = 0
        self.assertTrue(home_address.is_locality_valid())

        home_address.locality_id = 1
        self.assertTrue(home_address.is_locality_valid())


class ValidationTest(unittest.TestCase):
    def test_is_valid_returns_false_when_society_is_invalid(self):
        home_address = HomeAddress(society='', building='abc', flat_number='abc', locality_id=0)
        self.assertFalse(home_address.is_valid())

    def test_is_valid_returns_false_when_building_is_invalid(self):
        home_address = HomeAddress(society='abc', building='', flat_number='abc', locality_id=0)
        self.assertFalse(home_address.is_valid())

    def test_is_valid_returns_false_when_flat_number_is_invalid(self):
        home_address = HomeAddress(society='abc', building='abc', flat_number='', locality_id=0)
        self.assertFalse(home_address.is_valid())

    def test_is_valid_returns_false_when_locality_is_invalid(self):
        home_address = HomeAddress(society='abc', building='abc', flat_number='abc')
        self.assertFalse(home_address.is_valid())

    def test_is_valid_returns_true_when_everything_is_valid(self):
        home_address = HomeAddress(society='abc', building='abc', flat_number='abc', locality_id=0)
        self.assertTrue(home_address.is_valid())


if __name__ == '__main__':
    unittest.main()
