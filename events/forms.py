from django import forms 
from .models import *
from users.models import *

from datetime import date

CATEGORY_CHOICES = (
        ('Music', 'Music'),
        ('Cinema', 'Cinema'),
        ('Sport', 'Sport'),
    )


class EventForm(forms.Form):
    title = forms.CharField(
        label = "Title",
        max_length=150,
        widget= forms.TextInput(
            attrs= {
                'class':'form-control',
                'id': 'title',
                'placeholder': "Enter event title here"
            }
        )
    )
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORY_CHOICES)
    eventImage = forms.ImageField(label = "Image")
    nbrParticipants = forms.IntegerField(min_value=0, step_size=1)
    eventDate = forms.DateField(widget=forms.DateInput(attrs= {
                'class':'form-control date-input',
                'type': 'date'
            }        
    ))
    organizer = forms.ModelChoiceField(
        queryset=Person.objects.all()
    )
    
class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['state']
        help_texts = {
            'title': 'Enter title'
        }
    eventDate = forms.DateField(
        initial = date.today,
        widget=forms.DateInput(attrs= {
                'class':'form-control date-input',
                'type': 'date'
            }        
    ))
    category = forms.ChoiceField(widget=forms.RadioSelect, choices=CATEGORY_CHOICES)