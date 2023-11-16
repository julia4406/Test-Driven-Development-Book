from django.db import models

class Item(models.Model):
    # елемент списка
    text = models.TextField(default='')


