from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import unittest



class NewVisitorTest(unittest.TestCase):
    # A new user test, class based on Unittest

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_get_it_later(self):
        # New web-app with an urgent to-do list
        # Let's see on home-page
        self.browser.get('http://localhost:8000')

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
        time.sleep(1) # Page reload and appear new element in list: '1. Buy peacock feathers'

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1. Buy peacock feathers', [row.text for row in rows])


        # Text field suggest adding a new element
        # Type in text-field "Make a fishing fly with peacock feathers."
        # And press Enter
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Make a fishing fly with peacock feathers.')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1. Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2. Make a fishing fly with peacock feathers.', [row.text for row in rows])



        self.fail('Finish test!')

        # Page reload and appeared 2 elements in list.

        # You have to see the message with unique URL with explanations in use

        # Visit this URL and see your To-Do list there


if __name__ == '__main__':
    unittest.main(warnings='ignore')
