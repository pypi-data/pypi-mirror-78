import unittest
import uuid
from unittest import mock

from register.exceptions import *
from register.models import Customer, HomeAddress, OfficeAddress
from register.repository import RegisterRepository
from register.use_cases import register_customer, InvalidInput, CustomerAlreadyExists
from util.password import is_correct


# Done to avoid warning. 6-7 lines duplicated is not big deal in a test
# noinspection DuplicatedCode
class NeedBasedCustomerRegistration(unittest.TestCase):
    def test_register_raises_invalid_input_when_customer_is_none(self):
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        with self.assertRaises(InvalidInput):
            register_customer(None, home_address, office_address, 1, None)

    def test_register_raises_invalid_input_when_home_and_office_address_is_none(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')

        with self.assertRaises(InvalidInput):
            register_customer(customer, None, None, 1, None)

    def test_register_raises_invalid_input_when_cuisine_id_is_none(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        with self.assertRaises(InvalidInput):
            register_customer(customer, home_address, office_address, None, None)

    def test_register_raises_invalid_input_when_customer_is_invalid(self):
        customer = Customer()
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=0, company='abc')

        with self.assertRaises(InvalidInput):
            register_customer(customer, home_address, office_address, 1, None)

    def test_register_raises_invalid_input_when_home_address_is_invalid(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress()
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=0, company='abc')

        with self.assertRaises(InvalidInput):
            register_customer(customer, home_address, office_address, 1, None)

    def test_register_raises_invalid_input_when_home_address_is_invalid_without_office_address(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress()

        with self.assertRaises(InvalidInput):
            register_customer(customer, home_address, None, 1, None)

    def test_register_raises_invalid_input_when_office_address_is_invalid(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress()

        repository = mock.create_autospec(spec=RegisterRepository)
        repository.locality_exists.return_value = True

        with self.assertRaises(InvalidInput):
            register_customer(customer, home_address, office_address, 1, repository)

    def test_register_raises_invalid_input_when_office_address_is_invalid_without_home_address(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        office_address = OfficeAddress()

        with self.assertRaises(InvalidInput):
            register_customer(customer, None, office_address, 1, None)

    def test_register_raises_area_or_locality_does_not_exist_when_home_address_locality_does_not_exist(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        repository = mock.create_autospec(spec=RegisterRepository)
        repository.area_exists.return_value = True
        repository.locality_exists.return_value = False

        with self.assertRaises(AreaOrLocalityDoesNotExist):
            register_customer(customer, home_address, office_address, 1, repository)

        repository.locality_exists.assert_called_once_with(0)

    def test_register_raises_area_or_locality_does_not_exist_when_home_locality_does_not_exist_without_office_address(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)

        repository = mock.create_autospec(spec=RegisterRepository)
        repository.area_exists.return_value = False
        repository.locality_exists.return_value = False

        with self.assertRaises(AreaOrLocalityDoesNotExist):
            register_customer(customer, home_address, None, 1, repository)

        repository.locality_exists.assert_called_once_with(0)

    def test_register_raises_area_or_locality_does_not_exist_when_office_area_does_not_exist(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        repository = mock.create_autospec(spec=RegisterRepository)
        repository.locality_exists.return_value = True
        repository.area_exists.return_value = False

        with self.assertRaises(AreaOrLocalityDoesNotExist):
            register_customer(customer, home_address, office_address, 1, repository)

        repository.area_exists.assert_called_once_with(1)

    def test_register_raises_area_or_locality_does_not_exist_when_office_area_does_not_exist_no_home_address(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        repository = mock.create_autospec(spec=RegisterRepository)
        repository.area_exists.return_value = False

        with self.assertRaises(AreaOrLocalityDoesNotExist):
            register_customer(customer, None, office_address, 1, repository)

        repository.area_exists.assert_called_once_with(1)

    def test_register_raises_customer_already_exists_when_customer_exists(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        repository = mock.create_autospec(spec=RegisterRepository)

        repository.area_exists.return_value = True
        repository.locality_exists.return_value = True
        repository.customer_exists.return_value = True

        with self.assertRaises(CustomerAlreadyExists):
            register_customer(customer, home_address, office_address, 1, repository)

        repository.locality_exists.assert_called_once_with(0)
        repository.area_exists.assert_called_once_with(1)
        repository.customer_exists.assert_called_once_with('1234567890')

    def test_register_raises_cuisine_does_not_exist_when_cuisine_does_not_exist(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        repository = mock.create_autospec(spec=RegisterRepository)

        repository.area_exists.return_value = True
        repository.locality_exists.return_value = True
        repository.customer_exists.return_value = False
        repository.cuisine_exists.return_value = False

        with self.assertRaises(CuisineDoesNotExist):
            register_customer(customer, home_address, office_address, 1, repository)

        repository.locality_exists.assert_called_once_with(0)
        repository.area_exists.assert_called_once_with(1)
        repository.customer_exists.assert_called_once_with('1234567890')
        repository.cuisine_exists.assert_called_once_with(1)

    def test_success_without_home_address(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        repository = mock.create_autospec(spec=RegisterRepository)

        repository.area_exists.return_value = True
        repository.customer_exists.return_value = False
        repository.cuisine_exists.return_value = True

        cuisine_id = 1

        register_customer(customer, None, office_address, cuisine_id, repository)

        repository.area_exists.assert_called_once_with(1)
        repository.customer_exists.assert_called_once_with('1234567890')
        repository.cuisine_exists.assert_called_once_with(1)
        repository.insert.assert_called_once_with(customer, None, office_address, cuisine_id)

        # make sure password is hashed
        self.assertTrue(is_correct('0987654321', customer.password))

    def test_success_without_office_address(self):
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number='1234567890',
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)

        repository = mock.create_autospec(spec=RegisterRepository)

        repository.locality_exists.return_value = True
        repository.customer_exists.return_value = False
        repository.cuisine_exists.return_value = True

        cuisine_id = 1

        register_customer(customer, home_address, None, cuisine_id, repository)

        repository.locality_exists.assert_called_once_with(0)
        repository.customer_exists.assert_called_once_with('1234567890')
        repository.cuisine_exists.assert_called_once_with(1)
        repository.insert.assert_called_once_with(customer, home_address, None, cuisine_id)

        # make sure password is hashed
        self.assertTrue(is_correct('0987654321', customer.password))

    def test_success(self):
        pho_no = '1234567890'
        customer = Customer(first_name='abc', last_name='abc', email='abc@def.com', phone_number=pho_no,
                            password='0987654321')
        home_address = HomeAddress(flat_number='abc', building='abc', society='abc', locality_id=0)
        office_address = OfficeAddress(office_number='abc', floor=1, tower='abc', area_id=1, company='abc')

        repository = mock.create_autospec(spec=RegisterRepository)

        repository.area_exists.return_value = True
        repository.locality_exists.return_value = True
        repository.customer_exists.return_value = False
        repository.cuisine_exists.return_value = True
        customer_id = uuid.uuid4()
        repository.insert.return_value = customer_id

        cuisine_id = 1

        register_customer(customer, home_address, office_address, cuisine_id, repository)

        repository.locality_exists.assert_called_once_with(0)
        repository.area_exists.assert_called_once_with(1)
        repository.customer_exists.assert_called_once_with(pho_no)
        repository.cuisine_exists.assert_called_once_with(1)
        repository.insert.assert_called_once_with(customer, home_address, office_address, cuisine_id)

        # make sure password is hashed
        self.assertTrue(is_correct('0987654321', customer.password))


if __name__ == '__main__':
    unittest.main()
