"""
The main use case for register.

Contains just register_customer function
"""
import logging

from register.exceptions import AreaOrLocalityDoesNotExist, \
    CustomerAlreadyExists, \
    CuisineDoesNotExist
from util.exceptions import InvalidInput
from util.password import hash_password

logger = logging.getLogger(__name__)


def register_customer(customer, home_address, office_address, cuisine_id, repository):
    """
    Takes a customer, one or both of their home or office address and
    the cuisine id of their choice and registers the customer.

    Exceptions thrown -
        a) util.exceptions.InvalidInput is thrown when -
            1. Input contains null where it shouldn't
            2. A required field is omitted
            3. Customer, home address and/or office address are invalid
            4. Request body does not contain json
            5. You are trying to book a meal for a day it cannot be served on

        b) register.exceptions.AreaOrLocalityDoesNotExist is thrown when
        locality id or area id does not exist

        c) register.exceptions.CustomerAlreadyExists is thrown when customer
        already exists

        d) register.exceptions.CuisineDoesNotExist is thrown when cuisine
        id does not exist


    :param customer: customer to register
    :param home_address: home address of customer (conditionally nullable)
    :param office_address: office address of customer (conditionally nullable)
    :param cuisine_id: cuisine id of choice
    :param repository: repository to use
    :return: nothing. if register_customer does not throw, it succeeded
    """
    if customer is None or \
            cuisine_id is None:
        logger.info('customer or cuisine id is null')
        raise InvalidInput('Customer or cuisine id is null')

    if home_address is None and office_address is None:
        logger.info('both home address and customer address are none')
        raise InvalidInput('Both office and home address are nome')

    if not customer.is_valid():
        logger.info('customer is invalid')
        raise InvalidInput('Customer is invalid')

    if home_address is not None:
        if not home_address.is_valid():
            logger.info('home address is invalid')
            raise InvalidInput('Home address is invalid')

        if not repository.locality_exists(home_address.locality_id):
            logger.info('locality of home address does not exist')
            raise AreaOrLocalityDoesNotExist

    if office_address is not None:
        if not office_address.is_valid():
            logger.info('office address is not valid')
            raise InvalidInput('Office address is invalid')

        if not repository.area_exists(office_address.area_id):
            logger.info('area of office address does not exist')
            raise AreaOrLocalityDoesNotExist

    if repository.customer_exists(customer.phone_number):
        logger.info('customer already exists')
        raise CustomerAlreadyExists

    if not repository.cuisine_exists(cuisine_id):
        logger.info('cuisine does not exists')
        raise CuisineDoesNotExist

    # hash the password and store it in customer.password field again to store in database
    customer.password = hash_password(customer.password)

    # No effort made to ensure that this customer is not inserted
    # between customer exists call and insert. This is deliberately
    # done because it is not a realistic scenario and even if it
    # happens the database will raise a unique violation exception
    # aborting whatever transaction repository is using
    repository.insert(customer, home_address, office_address, cuisine_id)

    return True
