from django.test import TestCase
from django.urls import resolve

from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page, view_list
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        '''тест: використовується домашній шаблон'''
        response = self.client.get('/') #викликаєм client.get, та передаємо url для тестування
        self.assertTemplateUsed(response, 'home.html') #перевіряє який html-шаблон використовується

class ListAndItemModelTest(TestCase):
    # клас для тестування моделі елемента списку
    # створення нового запису в базі даних

    def test_saving_and_retrieving_items(self):
        # тест збереження та отримання елементів списку
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'The second item')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    '''Тест відображення списку'''

    def test_uses_list_template(self):
        ''' тест: є шаблон-сторінка list.html'''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        ''' тест: відображуються елементи тільки цього списка'''
        correct_list = List.objects.create()
        Item.objects.create(text='sprava 1', list=correct_list)
        Item.objects.create(text='sprava 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='zovsim_insha_sprava 1', list=other_list)
        Item.objects.create(text='zovsim_insha_sprava 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'sprava 1')
        self.assertContains(response, 'sprava 2')
        self.assertNotContains(response, 'zovsim_insha_sprava 1')
        self.assertNotContains(response, 'zovsim_insha_sprava 2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):
    '''тестовий клас для створення нового списку'''

    def test_can_save_a_POST_request(self):
        ''' тест: зберігаємо post-запрос'''
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)  # Впевнюємось що новий об'єкт Item збережено в БД
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')  # перевіряємо текст документа

    def test_redirects_after_POST(self):
        ''' тест: переадресація після post-запроса'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        ''' тест: зберігаємо post-запрос до існуючого списку'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)  # Впевнюємось що новий об'єкт Item збережено в БД
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')  # перевіряємо текст документа
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        ''' тест: переадресація в відображення списку'''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item',
                                    data={'item_text': 'A new item for an existing list'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')







