from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    # A new user test, class based on Unittest

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_get_it_later(self):
        # New web-app with an urgent to-do list
        # Let's see on home-page
        self.browser.get('http://localhost:8000')

        # there is title and head on page talk to us about
        # urgent to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Test finished!')  # never works and always generate error message

        # suggestion to add an item to the list

        # Type in text-field "Buy peacock feathers"

        # Press Enter
        # Page reload and appear new element in list: '1. Buy peacock feathers'

        # Text field suggest adding a new element

        # Type in text-field "Make a fishing fly with peacock feathers."

        # Press Enter
        # Page reload and appeared 2 elements in list.

        # You have to see the message with unique URL with explanations in use

        # Visit this URL and see your To-Do list there


if __name__ == '__main__':
    unittest.main(warnings='ignore')
