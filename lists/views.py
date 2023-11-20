from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    ''' функція відображення нового списку'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/unique_personal_list/')
