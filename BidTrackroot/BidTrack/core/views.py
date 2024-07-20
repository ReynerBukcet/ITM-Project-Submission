from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from geopy.distance import geodesic
from .forms import BidetForm, CustomUserCreationForm, LocationForm, ReviewForm
from .models import Bidet, Review, UserProfile
from django.http import JsonResponse
from django.contrib.auth import (login, logout, authenticate)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#Everything above this imports the dependencies for this file, whether from other files or functions of python/django/geopy) used for distance

@login_required
def home(request):
    return render(request, 'home.html')
#This is the home page, it requires a login tho guest log-in is also possible, all it does is render home.html

@login_required
def add_bidet(request):
    if request.method == 'POST':
        form = BidetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BidetForm()
    
    return render(request, 'add_bidet.html', {'form': form, 'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})
#This is the function that adds bidets to the database, it loads the BidetForm form in form.py, and also feeds the Google maps API key to the html

@login_required
def find_bidets(request):
    form = LocationForm(request.GET)
    if form.is_valid():
        user_lat = form.cleaned_data['latitude']
        user_long = form.cleaned_data['longitude']
        user_location = (user_lat, user_long)
        
        user_time_str = request.GET.get('user_time')
        if user_time_str:
            user_time = datetime.datetime.strptime(user_time_str, '%H:%M').time()
        else:
            user_time = timezone.now().time()

        bidets = Bidet.objects.filter(opening_time__lte=user_time, closing_time__gte=user_time)

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            needs_handicap_access = user_profile.needs_handicap_access
        except UserProfile.DoesNotExist:
            needs_handicap_access = False

        if needs_handicap_access:
            bidets = bidets.filter(handicap_friendly=True)

        bidet_distances = []

        for bidet in bidets:
            bidet_location = (bidet.latitude, bidet.longitude)
            distance = geodesic(user_location, bidet_location).km
            bidet_distances.append((bidet, distance))

        bidet_distances.sort(key=lambda x: x[1])
        nearest_bidets = [bidet for bidet, distance in bidet_distances[:5]]  

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            bidet_data = [
                {
                    'name': bidet.name,
                    'address': bidet.address,
                    'latitude': bidet.latitude,
                    'longitude': bidet.longitude,
                    'handicap_friendly': bidet.handicap_friendly,
                    'opening_time': bidet.opening_time.strftime('%H:%M'),
                    'closing_time': bidet.closing_time.strftime('%H:%M')
                }
                for bidet in nearest_bidets
            ]
            return JsonResponse(bidet_data, safe=False)
        else:
            return render(request, 'find_bidets.html', {'bidets': nearest_bidets, 'user_location': user_location, 'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})
    else:
        return render(request, 'find_bidets.html', {'error': 'Please wait for the map to load. Kindly reload the page if not loading.', 'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY})
#This is the Find a bidet views (the one that loads when you click the find bidet from home), The things it does is (with the help of the html template and scripts): gets the users location, get the date time, Check the user's handicap access need, filters it to 5 nearest, only open, handicap need, and sorts it by distance, and displays buttons of the bidets that redirects to the specific buttons page.

@login_required
def bidet_detail(request, bidet_name):
    bidet = get_object_or_404(Bidet, name=bidet_name)
    reviews = Review.objects.filter(bidet=bidet)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.bidet = bidet
            review.user = request.user
            review.save()
            return redirect('bidet_detail', bidet_name=bidet_name)
    else:
            form = ReviewForm()
    
    return render(request, 'bidet_detail.html', {
        'bidet': bidet,
        'reviews': reviews,
        'form': form,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    })
#This is the function that makes a page for every bidet, it also contains the review forms where users can leave reviews for the specific bidets, and it also loads the map and directions that shows the way from the user's location to the location of the bidet they clicked.

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login_view.html')
    elif request.method == 'POST':
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']
        user_object = authenticate(
            username=submitted_username,
            password=submitted_password
        )
        if user_object is None:
            messages.add_message(request, messages.INFO, 'Invalid login.')
            return redirect(request.path_info)
        login(request, user_object)
        return redirect('home')
#This is the login_view which lets users login, mostly inspired from digital cafe 
  
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST' and review.user == request.user:
        review.delete()
    return redirect('bidet_detail', bidet_name=review.bidet.name)
#This lets user delete their reviews

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            needs_handicap_access = form.cleaned_data.get('needs_handicap_access')
            UserProfile.objects.create(user=user, needs_handicap_access=needs_handicap_access)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
#This lets user register to create an account, it uses the builtin django user but also modified a bit to include our handicap function

def guest_login(request):
    guest_user, created = User.objects.get_or_create(username='guest')
    if created:
        guest_user.set_password(User.objects.make_random_password())
        guest_user.save()
    login(request, guest_user)
    return redirect('home')
#This lets users log-in as guest if they do not have an account and it is a poop emergency