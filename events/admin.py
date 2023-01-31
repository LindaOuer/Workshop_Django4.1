from django.contrib import admin
from .models import *


# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'state'
    )
    ordering = ('title',)
    list_filter = ('state', 'category')
    


admin.site.register(Event, EventAdmin)
