from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    if request.method == 'POST': # new-item_tex буде зберігати вміст POST-запиту або пусто
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/unique_personal_list/')
    return render(request, 'home.html')


def view_list(request):
    ''' функція відображення нового списку'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})



