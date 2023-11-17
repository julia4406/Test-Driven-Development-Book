from django.shortcuts import render, redirect
from lists.models import Item

def home_page(request):
    if request.method == 'POST': # new-item_tex буде зберігати вміст POST-запиту або пусто
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})






