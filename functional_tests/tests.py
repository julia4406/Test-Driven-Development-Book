from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import time
import os

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    # A new user test, class based on Unittest

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self) -> None:
        #self.browser.refresh()
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

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # start a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')  # Type in text-field "Buy peacock feathers"
        inputbox.send_keys(Keys.ENTER) # Press Enter
        # Page reload and appear new element in list: '1. Buy peacock feathers'
        self.wait_for_row_in_list_table('1. Buy peacock feathers')

        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')

        # adding new user
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Make a fishing fly with peacock feathers.', page_text)

        # new user starts new list
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy milk')

        user2_list_url = self.browser.current_url   # user2 got new url-addr
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        # Page reload and appeared 2 elements in list.
        # You have to see the message with unique URL with explanations in use
        # Visit this URL and see your To-Do list there

    def test_layout_and_styling(self):
        ''' тестуємо макет та стильове оформлення'''
        # user open home-page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # the input-form-fild is centered
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] +
                               inputbox.size['width'] / 2, 512, delta=10)

        # start new list, the input-form-fild is centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. testing')
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] +
                               inputbox.size['width'] / 2, 512, delta=10)

