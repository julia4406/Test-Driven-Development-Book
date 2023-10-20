from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

# test for testing tests ))
'''
class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
'''

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # url становиться домашньою сторінкою
        found = resolve('/')
        self.assertEqual(found.func, home_page)

