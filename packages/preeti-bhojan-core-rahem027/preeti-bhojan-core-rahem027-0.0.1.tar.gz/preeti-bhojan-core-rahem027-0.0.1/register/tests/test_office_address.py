import unittest

from register.models import OfficeAddress, InvalidInput
from register.tests.input import alphaNumericWithSpacesAndUnderscore


class JsonTest(unittest.TestCase):
    def test_from_json(self):
        office_address = OfficeAddress.from_json(
            {
                'office_number': '123',
                'floor': 1,
                'tower': 'abc',
                'area_id': 1,
                'company': 'def'
            }
        )

        self.assertEqual(office_address.office_number, '123')
        self.assertEqual(office_address.floor, 1)
        self.assertEqual(office_address.tower, 'abc')
        self.assertEqual(office_address.area_id, 1)
        self.assertEqual(office_address.company, 'def')


class NoneTest(unittest.TestCase):
    def test_constructor_throws_invalid_input_when_office_number_is_none(self):
        with self.assertRaises(InvalidInput):
            OfficeAddress(None, 0, '', 0)

    def test_constructor_throws_invalid_input_when_floor_is_none(self):
        with self.assertRaises(InvalidInput):
            OfficeAddress('', None, '', 0)

    def test_constructor_throws_invalid_input_when_tower_is_none(self):
        with self.assertRaises(InvalidInput):
            OfficeAddress('', 0, None, 0)

    def test_constructor_throws_invalid_input_when_area_id_is_none(self):
        with self.assertRaises(InvalidInput):
            OfficeAddress('', 0, '', None)


class IndividualFieldsTest(unittest.TestCase):
    def test_office_number_should_contain_alphabets_numbers_underscore_and_space(self):
        for office_number, isValid in alphaNumericWithSpacesAndUnderscore.items():
            office_address = OfficeAddress(office_number=office_number)
            self.assertEqual(office_address.is_office_number_valid(), isValid)

    def test_floor_be_a_number_greater_than_0(self):
        office_address = OfficeAddress(floor=-13)
        self.assertFalse(office_address.is_floor_valid())

        office_address.floor = 12
        self.assertTrue(office_address.is_floor_valid())
            
    def test_tower_should_contain_alphabets_numbers_underscore_and_space(self):
        for tower, isValid in alphaNumericWithSpacesAndUnderscore.items():
            office_address = OfficeAddress(tower=tower)
            self.assertEqual(office_address.is_tower_valid(), isValid)

    def test_area_id_should_not_be_negative(self):
        # By default, area_id is -1 which is invalid
        office_address = OfficeAddress()
        self.assertFalse(office_address.is_area_valid())

        office_address.area_id = 0
        self.assertTrue(office_address.is_area_valid())

        office_address.area_id = 1
        self.assertTrue(office_address.is_area_valid())


class ValidationTest(unittest.TestCase):
    def test_is_valid_should_be_false_when_office_number_is_invalid(self):
        office_address = OfficeAddress(office_number='', floor=12, tower='abc', area_id=0)
        self.assertFalse(office_address.is_valid())

    def test_is_valid_should_be_false_when_floor_is_invalid(self):
        office_address = OfficeAddress(office_number='abc', floor=-12, tower='abc', area_id=0)
        self.assertFalse(office_address.is_valid())

    def test_is_valid_should_be_false_when_tower_is_invalid(self):
        office_address = OfficeAddress(office_number='abc', floor=12, tower='', area_id=0)
        self.assertFalse(office_address.is_valid())

    def test_is_valid_should_be_false_when_area_is_invalid(self):
        office_address = OfficeAddress(office_number='abc', floor=12, tower='abc')
        self.assertFalse(office_address.is_valid())

            
if __name__ == '__main__':
    unittest.main()
