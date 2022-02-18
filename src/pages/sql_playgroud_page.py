from framework.web_element import WebElement
from framework.web_page import WebPage

from src.data_for_testing.sql_playground_data import TABLE


class SQLPage(WebPage):

    def __init__(self):
        self.url = 'https://www.w3schools.com/sql/trysql.asp?filename=trysql_asc'
        super().__init__('[id = resultSQL]', name='SQL playground page')

    # Page mixin elements

    def run_sql_button(self):
        return WebElement('//button[.="Run SQL »"]', name='run sql button')

    def restore_database_button(self):
        return WebElement('button[title *= "Restore the database"]', name='restore database button')

    def database_changed_info(self):
        return WebElement('//*[contains(., "You have made changes to the database.")]',
                          name='database changed info')

    def database_restored_info(self):
        return WebElement('//*[.="The database is fully restored."]', name='database restored info')

    # Popup table (top-right corner)

    def customers_records_count(self):
        return WebElement('//*[@id="yourDB"]//tr[contains(., "Customers")]//td[2]',
                          name='records count from popup table').get_text()

    # Result table elements

    def any_table_row(self):
        return WebElement('//*[@id="resultSQL"]//tr[.//td]', name='any table row')

    def row_by_contact_name(self, customer_name):
        return WebElement(f'//tr[contains(., "{customer_name}")]',
                          name=f'table row by contact name: {customer_name}')

    # Result table getters

    def get_customer_id_by_contact_name(self, customer_name):
        return WebElement(f'//tr[contains(., "{customer_name}")]//td[1]',
                          name=f'customer id by contact name: {customer_name}').get_text()

    def get_customer_name_by_contact_name(self, customer_name):
        return WebElement(f'//tr[contains(., "{customer_name}")]//td[2]',
                          name=f'customer name by contact name: "{customer_name}"').get_text()

    def get_address_by_contact_name(self, customer_name):
        return WebElement(f'//tr[contains(., "{customer_name}")]//td[4]',
                          name=f'address by contact name: "{customer_name}"').get_text()

    def get_city_by_contact_name(self, customer_name):
        return WebElement(f'//tr[contains(., "{customer_name}")]//td[5]',
                          name=f'city by contact name: "{customer_name}"').get_text()

    def get_code_by_contact_name(self, customer_name):
        return WebElement(f'//tr[contains(., "{customer_name}")]//td[6]',
                          name=f'postal code by customer name: "{customer_name}"').get_text()

    def get_county_by_contact_name(self, customer_name):
        return WebElement(f'//tr[contains(., "{customer_name}")]//td[7]',
                          name=f'country by contact name: "{customer_name}"').get_text()

    # Functions

    def get_all_customers_table_data(self):
        """
        Get all data from Customers table

        :return: self object
        """
        self.driver_wrapper.clear_text_from_editor().type_text_to_editor(f'SELECT * FROM {TABLE}')
        self.run_sql_button().click()
        return self

    def send_new_sql_command(self, sql_command, wait=True):
        """
        Send new sql command into database

        :param sql_command: sql command to send
        :param wait: wait presence of "You have made changes ..." caption
        :return: self object
        """
        self.driver_wrapper.clear_text_from_editor().type_text_to_editor(sql_command)
        self.run_sql_button().click()
        if wait:
            self.database_changed_info().wait_element()
        return self

    def get_all_rows_count(self):
        """
        Get all current rows count. Opens default table if nothing available

        :return: int object - rows count
        """
        if not self.any_table_row().is_available():
            self.get_all_customers_table_data()
        return int(self.customers_records_count())
