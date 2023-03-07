from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import *
from users.models import Person
from .forms import EventForm, EventModelForm
# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


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


@login_required(login_url='/account/login')
def listEvents(request):
    # list = Event.objects.all()
    list = Event.objects.filter(state=True)
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


def participateEvent(request, id):
    event = Event.objects.get(id=id)
    # person = Person.objects.get(cin='12345679')
    person = request.user

    if Participation.objects.filter(person=person, event=event).count() == 0:
        Participation.objects.create(person=person, event=event)

        event.nbrParticipants += 1
        event.save()

        # nb = event.nbrParticipants + 1
        # Event.objects.filter(id=id).update(nbrParticipants=nb)

    return redirect("events_list")


def cancelEvent(request, id):
    event = Event.objects.get(id=id)
    person = Person.objects.get(cin='12345679')
    participation = Participation.objects.filter(person=person, event=event)
    if participation.count() != 0:
        participation.delete()

        event.nbrParticipants -= 1
        event.save()
        # messages.add_message(request, messages.SUCCESS, f'Your participation has been revoked \"{event.title}\"')

        # nb = event.nbrParticipants + 1
        # Event.objects.filter(id=id).update(nbrParticipants=nb)

    return redirect("events_list")


def deleteEvent(request, id):
    Event.objects.get(id=id).delete()
    return redirect("events_list")

# class


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventModelForm
    success_url = reverse_lazy('events_list')
    login_url = 'login'


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventModelForm
    success_url = reverse_lazy('events_list')
    template_name = 'events/events_add.html'


class EventsList(ListView):
    model = Event
    template_name = 'events/listEvents.html'
    context_object_name = 'events'
    queryset = Event.objects.filter(state=True)
    # def get_queryset(self):
    #     return  Event.objects.filter(state=True)


class EventsDetails(DetailView):
    model = Event


class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('events_list')
