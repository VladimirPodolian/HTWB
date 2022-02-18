from random import choice

import pytest

from src.pages.sql_playgroud_page import SQLPage
from src.data_for_testing.sql_playground_data import (
    random_data, CONTACT_NAME_COLUMN, CUSTOMER_NAME_COLUMN,
    ADDRESS_COLUMN, CITY_COLUMN, POSTAL_CODE_COLUMN, COUNTRY_COLUMN,
    TABLE, CUSTOMER_ID_COLUMN,
)


@pytest.fixture
def page():
    """ Get sql playground page """
    return SQLPage().open_page()


@pytest.fixture
def get_insert_sql_command(page):
    """ Get INSERT sql command dependent on current rows count """
    random_data['CustomerID'] = str(page.get_all_rows_count() + 1)  # Set available id
    return f"INSERT INTO {TABLE} VALUES {str(tuple(random_data.values()))}"


@pytest.fixture
def get_random_row_id(page):
    """ Get random row id dependent on current rows count """
    return choice(range(1, page.get_all_rows_count() + 1))


@pytest.fixture
def get_update_sql_command(get_random_row_id):
    """ Get UPDATE sql command with random row id """
    random_data.pop(CUSTOMER_ID_COLUMN)  # Do not update id of the row
    get_set_values = ', '.join(f'{key}="{value}"' for key, value in random_data.items())
    return f'UPDATE {TABLE} SET {get_set_values} WHERE {CUSTOMER_ID_COLUMN}={get_random_row_id}'


def test_sql_playground_check_address(page):
    """
    Вывести все строки таблицы Customers и убедиться, что запись с ContactName
      равной ‘Giovanni Rovelli’ имеет Address = ‘Via Ludovico il Moro 22’.
    """
    page.get_all_customers_table_data()
    assert page.get_address_by_contact_name('Giovanni Rovelli') == 'Via Ludovico il Moro 22'


def test_sql_playground_specific_city(page):
    """
    Вывести только те строки таблицы Customers, где city=‘London’.
    Проверить, что в таблице ровно 6 записей.
    """
    page.send_new_sql_command(f'SELECT * FROM {TABLE} WHERE City = "London"', wait=False)
    assert page.any_table_row().get_elements_count() == 6


def test_sql_playground_insert_and_select(page, get_insert_sql_command):
    """
    Добавить новую запись в таблицу Customers и проверить, что эта запись добавилась.
    """
    page.send_new_sql_command(get_insert_sql_command)
    page.get_all_customers_table_data()
    assert page.row_by_contact_name(random_data[CONTACT_NAME_COLUMN]).wait_element().is_displayed()


def test_sql_playground_change_and_select(page, get_update_sql_command, get_random_row_id):
    """
    Обновить все поля (кроме CustomerID) в любой записи таблицы Customers
      и проверить, что изменения записались в базу.
    """
    page.send_new_sql_command(get_update_sql_command)
    page.get_all_customers_table_data()
    assert (
        page.get_customer_id_by_contact_name(random_data[CONTACT_NAME_COLUMN]),
        page.get_customer_name_by_contact_name(random_data[CONTACT_NAME_COLUMN]),
        page.get_address_by_contact_name(random_data[CONTACT_NAME_COLUMN]),
        page.get_city_by_contact_name(random_data[CONTACT_NAME_COLUMN]),
        page.get_code_by_contact_name(random_data[CONTACT_NAME_COLUMN]),
        page.get_county_by_contact_name(random_data[CONTACT_NAME_COLUMN]),
    ) == (
        str(get_random_row_id),
        random_data[CUSTOMER_NAME_COLUMN],
        random_data[ADDRESS_COLUMN],
        random_data[CITY_COLUMN],
        random_data[POSTAL_CODE_COLUMN],
        random_data[COUNTRY_COLUMN],
    )


def test_sql_playground_drop_table_and_restore(wrapped_driver, page):
    """
    Cобственный автотест.
    Сброс таблицы Customers и последующее восстановление.
    """
    page.send_new_sql_command(f'DROP TABLE {TABLE}')

    # Trying to get dropped table
    page.get_all_customers_table_data()
    wrapped_driver.wait_alert().accept_alert()

    # Restore database
    page.restore_database_button().click()
    wrapped_driver.wait_alert().accept_alert()

    assert page.database_restored_info().wait_element().is_displayed()
