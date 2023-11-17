from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    # A new user test, class based on Unittest

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_get_it_later(self):
        # New web-app with an urgent to-do list
        # Let's see on home-page
        self.browser.get(self.live_server_url)

        # there is title and head on page talk to us about
        # urgent to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # suggestion to add an item to the list
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        inputbox.send_keys('Buy peacock feathers')  # Type in text-field "Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER) # Press Enter
        # Page reload and appear new element in list: '1. Buy peacock feathers'
        self.wait_for_row_in_list_table('1. Buy peacock feathers')

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1. Buy peacock feathers', [row.text for row in rows])


        # Text field suggest adding a new element
        # Type in text-field "Make a fishing fly with peacock feathers."
        # And press Enter
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Make a fishing fly with peacock feathers.')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1. Buy peacock feathers')
        self.wait_for_row_in_list_table('2. Make a fishing fly with peacock feathers.')

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1. Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2. Make a fishing fly with peacock feathers.', [row.text for row in rows])



        self.fail('Finish test!')

        # Page reload and appeared 2 elements in list.

        # You have to see the message with unique URL with explanations in use

        # Visit this URL and see your To-Do list there


