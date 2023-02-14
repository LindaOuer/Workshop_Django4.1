from django.shortcuts import render
from django.http import HttpResponse

from .models import Event
# Create your views here.


def homePage(request):
    return HttpResponse('<h1>Welcome To... </h1>')


def listEventsStatic(request):
    list = [
        {
            'title': 'Event 1',
            'description': 'description 1',
        },
        {
            'title': 'Event 2',
            'description': 'description 2',
        },
        {
            'title': 'Event 3',
            'description': 'description 3',
        }
    ]
    return render(
        request,
        'events/listEvents.html',
        {
            'events': list,
        }
    )


def listEvents(request):
    list = Event.objects.all()
    return render(
        request,
        'events/listEvents.html',
        {
            'events': list,
        }
    )
