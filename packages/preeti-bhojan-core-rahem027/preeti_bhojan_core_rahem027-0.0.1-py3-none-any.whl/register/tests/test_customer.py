import unittest

from register.models import Customer, InvalidInput
from register.tests.input import alphabetic, phoneNumbers


class JsonTest(unittest.TestCase):
    def test_from_json(self):
        customer = Customer.from_json({
            'first_name': 'abc',
            'last_name': 'def',
            'email': 'abc@def.com',
            'phone_number': '012',
            'password': 'pass'
        })
        self.assertEqual(customer.first_name, 'abc')
        self.assertEqual(customer.last_name, 'def')
        self.assertEqual(customer.email, 'abc@def.com')
        self.assertEqual(customer.phone_number, '012')
        self.assertEqual(customer.password, 'pass')


class NoneTest(unittest.TestCase):
    def test_constructor_throws_invalid_input_if_first_name_is_none(self):
        with self.assertRaises(InvalidInput):
            Customer(None, '', '', '', '')

    def test_constructor_throws_invalid_input_if_last_name_is_none(self):
        with self.assertRaises(InvalidInput):
            Customer('', None, '', '', '')

    def test_constructor_throws_invalid_input_if_company_is_none(self):
        with self.assertRaises(InvalidInput):
            Customer('', '', None, '', '')

    def test_constructor_throws_invalid_input_if_phone_number_is_none(self):
        with self.assertRaises(InvalidInput):
            Customer('', '', '', None, '')

    def test_constructor_throws_invalid_input_if_password_is_none(self):
        with self.assertRaises(InvalidInput):
            Customer('', '', '', '', None)


class IndividualFieldsTest(unittest.TestCase):
    def test_first_name_should_be_alphabetic(self):
        for firstName, isValid in alphabetic.items():
            customer = Customer(first_name=firstName)
            self.assertEqual(customer.is_first_name_valid(), isValid)

    def test_last_name_should_be_alphabetic(self):
        for lastName, isValid in alphabetic.items():
            customer = Customer(last_name=lastName)
            self.assertEqual(customer.is_last_name_valid(), isValid)

    def test_email_must_be_valid(self):
        for email, isValid in {
            'abc@def.com': True,
            'abc': False
        }.items():
            customer = Customer(email=email)
            self.assertEqual(customer.is_email_valid(), isValid)

    def test_phone_number_must_be_10_digit_must_contain_alphabets_numbers(self):
        for phoneNumber, isValid in phoneNumbers.items():
            customer = Customer(phone_number=phoneNumber)
            self.assertEqual(customer.is_phone_number_valid(), isValid)

    def test_password_should_be_at_least_8_characters_long(self):
        # Password greater than 8 characters
        customer = Customer(password='123456789')
        self.assertTrue(customer.is_password_valid())

        # 8 char long password
        customer.password = '12345678'
        self.assertTrue(customer.is_password_valid())

        # less than 8 char long password
        customer.password = '12'
        self.assertFalse(customer.is_password_valid())

    def test_password_above_70_characters_should_be_invalid(self):
        password = ''
        for num in range(71):
            password += str(num)

        customer = Customer(password=password)
        self.assertFalse(customer.is_password_valid())


class ValidationTest(unittest.TestCase):
    def test_is_valid_should_return_false_when_first_name_is_invalid(self):
        # Never use this password ;)
        customer = Customer(first_name='', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        self.assertFalse(customer.is_valid())

    def test_is_valid_should_return_false_when_last_name_is_invalid(self):
        customer = Customer(first_name='abc', last_name='', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        self.assertFalse(customer.is_valid())

    def test_is_valid_should_return_false_when_company_is_invalid(self):
        customer = Customer(first_name='abc', last_name='abc', email='', phone_number='1234567890',
                            password='0987654321')
        self.assertFalse(customer.is_valid())

    def test_is_valid_should_return_false_when_phone_number_is_invalid(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='',
                            password='0987654321')
        self.assertFalse(customer.is_valid())

    def test_is_valid_should_return_false_when_password_is_invalid(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='')
        self.assertFalse(customer.is_valid())

    def test_is_valid_should_return_true_when_everything_is_valid(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        self.assertTrue(customer.is_valid())


if __name__ == '__main__':
    unittest.main()
