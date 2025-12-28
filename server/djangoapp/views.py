# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate

from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})
    
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request, state=None):
    """Get dealerships - accepts state as optional path parameter"""
    # If state comes from path parameter, use it
    # Otherwise, check query parameter
    if not state:
        state = request.GET.get('state', None)
    
    print(f"get_dealerships called with state: {state}")
    
    if state and "All" in state:
        endpoint = "/fetchDealers"
    elif state:
        import re
        # Extract state names (capitalized words)
        states = re.findall(r'[A-Z][a-z]+', state)
        
        if states:
            # For now, use the first state found
            endpoint = f"/fetchDealers/{states[0]}"
        else:
            # If no state found, get all
            endpoint = "/fetchDealers"
    else:
        # No state provided
        endpoint = "/fetchDealers"
    
    print(f"Calling endpoint: {endpoint}")
    dealerships = get_request(endpoint)
    
    # Check for error
    if isinstance(dealerships, dict) and "error" in dealerships:
        print(f"Error from get_request: {dealerships['error']}")
        return JsonResponse({"status": 200, "dealers": []})
    
    # Ensure we return a list
    if not isinstance(dealerships, list):
        print(f"Warning: dealerships is not a list, it's {type(dealerships)}")
        dealerships = []
    
    return JsonResponse({"status": 200, "dealers": dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
"""def get_dealer_reviews(request,dealer_id):
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})"""

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        
        if isinstance(reviews, dict) and "error" in reviews:
            return JsonResponse({"status": 200, "reviews": []})
        
        if not isinstance(reviews, list):
            reviews = []
        
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            if response and 'sentiment' in response:
                review_detail['sentiment'] = response['sentiment']
            else:
                review_detail['sentiment'] = {"label": "neutral", "score": 0.5}
        
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        # Get all dealers and find the specific one
        endpoint = "/fetchDealers"
        all_dealers = get_request(endpoint)
        
        if isinstance(all_dealers, dict) and "error" in all_dealers:
            return JsonResponse({
                "status": 500, 
                "message": "Failed to fetch dealers",
                "dealer": {}
            })
        
        if not isinstance(all_dealers, list):
            all_dealers = []
        
        # Find dealer by ID
        dealer = None
        for d in all_dealers:
            if (d.get('id') == dealer_id or 
                d.get('dealership') == dealer_id):
                dealer = d
                break
        
        if dealer:
            return JsonResponse({
                "status": 200, 
                "dealer": {
                    "full_name": dealer.get('full_name', f'Dealer {dealer_id}'),
                    "city": dealer.get('city', 'Unknown'),
                    "address": dealer.get('address', 'Unknown'),
                    "zip": dealer.get('zip', '00000'),
                    "state": dealer.get('state', 'Unknown')
                }
            })
        else:
            # Dealer not found
            return JsonResponse({
                "status": 200,  # Still 200, but with placeholder
                "dealer": {
                    "full_name": f"Dealer {dealer_id}",
                    "city": "San Francisco",
                    "address": "123 Main St",
                    "zip": "94101",
                    "state": "CA"
                }
            })
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
