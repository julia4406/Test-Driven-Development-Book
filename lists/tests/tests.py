from django.test import TestCase
from django.urls import resolve

from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # url стає домашньою сторінкою
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        '''тест: використовується домашній шаблон'''
        response = self.client.get('/') #викликаєм client.get, та передаємо url для тестування
        self.assertTemplateUsed(response, 'home.html') #перевіряє який html-шаблон використовується

    def test_can_save_a_POST_request(self):
        ''' тест: зберігаємо post-запрос'''
        self.client.post('/', data={'item_text': 'A new list item'})

        # наступні 3 строки- представление має зберігати новий елемент в БД, а не передавати його
        # у відповідний відгук
        self.assertEqual(Item.objects.count(), 1) # Впевнюємось що новий об'єкт Item збережено в БД
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item') # перевіряємо текст документа

    def test_redirects_after_POST(self):
        ''' тест: переадресація після post-запроса'''
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        # тест: зберігає елементи тільки за потреби
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        ''' тест: відображуються всі елементи списка'''
        Item.objects.create(text='sprava 1')
        Item.objects.create(text='sprava 2')

        response = self.client.get('/')

        self.assertIn('sprava 1', response.content.decode())
        self.assertIn('sprava 2', response.content.decode())



class ItemModelTest(TestCase):
    # клас для тестування моделі елемента списку
    # створення нового запису в базі даних

    def test_saving_and_retrieving_items(self):
        # тест збереження та отримання елементів списку
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'The second item')





