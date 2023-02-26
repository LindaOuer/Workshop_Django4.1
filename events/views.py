from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Event
from .forms import EventForm, EventModelForm
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
    
def detailsEvent(request, id):
    event = Event.objects.get(id=id)
    return render(
        request,
        'events/event_detail.html',
        {
            'event': event,
        }
    )
    
def addEvent(request):
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            Event.objects.create(**form.cleaned_data)
            return redirect("events_list")
    return render(request, 'events/events_add.html', {'form': form})


def addEventModel(request):
    form = EventModelForm()
    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("events_list")
    return render(request, 'events/events_add.html', {'form': form})


# class 
class EventCreateView(CreateView):
    model = Event
    form_class = EventModelForm
    success_url = reverse_lazy('events_list')
class EventsList(ListView):
    model = Event
    template_name = 'events/listEvents.html'
    context_object_name = 'events'

class EventsDetails(DetailView):
    model = Event