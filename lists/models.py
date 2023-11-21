from django.db import models

class List(models.Model):
    # список
    #text = models.TextField(default='')
    pass

class Item(models.Model):
    # елемент списка
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)


