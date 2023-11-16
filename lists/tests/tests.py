from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # url становиться домашньою сторінкою
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        '''тест: використовується домашній шаблон'''
        response = self.client.get('/') #викликаєм client.get, та передаємо url для тестування
        self.assertTemplateUsed(response, 'home.html') #перевіряє який html-шаблон використовується

    def test_can_save_a_POST_request(self):
        ''' тест: зберігаємо post-запрос'''
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')



