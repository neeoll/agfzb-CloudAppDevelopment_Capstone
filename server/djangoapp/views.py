from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    context = {}
    if (request.method == 'GET'):
        return render(request, 'djangoapp/index.html', context)


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if (request.method == 'GET'):
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if (request.method == 'GET'):
        return render(request, 'djangoapp/contact.html', context)
        
# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if (request.method == "GET"):
        return render(request, 'djangoapp/registration.html', context)
    elif (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New User")
        if not user_exist:
            user = User.objects.create(
                username=username, 
                first_name=first_name, 
                last_name=last_name, 
                password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if (request.method == "GET"):
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/846eb439-3586-4d7d-82bd-3f206faf52b5/dealerships/get-dealerships.json"
        dealerships = get_dealers_from_cf(url)
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if (request.method == "GET"):
        url = f"https://us-south.functions.appdomain.cloud/api/v1/web/846eb439-3586-4d7d-82bd-3f206faf52b5/reviews/get-reviews.json?dealerId={dealer_id}"
        details = get_dealer_reviews_from_cf(url)
        review_names = ' '.join([review["name"] for review in details])
        return HttpResponse(details)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

