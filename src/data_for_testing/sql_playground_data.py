from random import choice

from src.utils import random_string


TABLE = 'Customers'
CUSTOMER_ID_COLUMN = 'CustomerID'
CUSTOMER_NAME_COLUMN = 'CustomerName'
CONTACT_NAME_COLUMN = 'ContactName'
ADDRESS_COLUMN = 'Address'
CITY_COLUMN = 'City'
POSTAL_CODE_COLUMN = 'PostalCode'
COUNTRY_COLUMN = 'Country'

customer_names = ['Ann Handel', 'Gourmet Accorti', 'Hanari Bennett']
contact_names = ['Tom Sanders', 'Francisc Brown', 'Diego Müller']
addresses = ['Oberes Str. 145', '244, place Bouchers', 'C/ Araquily, 05']
cities = ['Moscow', 'Limassol', 'Berlin', 'Tallinn']
random_postal_code = random_string(length=(5, 8))
countries = ['Russia', 'Republic of Cyprus', 'Germany', 'Estonia']

random_data = {
    CUSTOMER_ID_COLUMN: None,
    CUSTOMER_NAME_COLUMN: choice(customer_names),
    CONTACT_NAME_COLUMN: choice(contact_names),
    ADDRESS_COLUMN: choice(addresses),
    CITY_COLUMN: choice(cities),
    POSTAL_CODE_COLUMN: random_postal_code,
    COUNTRY_COLUMN: choice(countries),
}
