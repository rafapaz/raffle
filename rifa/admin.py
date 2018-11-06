from django.contrib import admin

from .models import Category, Raffle, Choice, Image, Reputation, Question

admin.site.register(Category)
admin.site.register(Raffle)
admin.site.register(Choice)
admin.site.register(Image)
admin.site.register(Reputation)
admin.site.register(Question)
