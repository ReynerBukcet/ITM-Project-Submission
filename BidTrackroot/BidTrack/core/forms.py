from django import forms
from .models import Bidet, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BidetForm(forms.ModelForm):
    handicap_friendly = forms.BooleanField(label='For handicapped users', required=False)

    class Meta:
        model = Bidet
        fields = ['name', 'latitude', 'longitude', 'address', 'handicap_friendly', 'opening_time', 'closing_time']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'address': forms.HiddenInput(),
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }
#This is the bidet form forms, it helps with adding bidets to our database it gets the things listed in the fields, the widgets helps with the functions in html (auto getting of location thru google maps api) and time        


class LocationForm(forms.Form):
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    address = forms.CharField(widget=forms.HiddenInput())
#This is the LocationF form it is used in our find bidet for automatically getting the latitude, longitude and address of the user with the help of google maps and geolocation 

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
#This is the reviewform, it gets the user's rating and comment

class CustomUserCreationForm(UserCreationForm):
    needs_handicap_access = forms.BooleanField(required=False, label='Do you need handicap access?')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'needs_handicap_access']
#This is the form we use to track the handicap access