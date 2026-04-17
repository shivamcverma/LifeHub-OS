from django.contrib import admin
from .models import Document, Expense, Reminder, Subscription

# Register your models here.
admin.site.register(Document)
admin.site.register(Expense)
admin.site.register(Reminder)
admin.site.register(Subscription)
