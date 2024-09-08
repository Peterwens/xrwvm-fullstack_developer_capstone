from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging
import json
from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_request` view to handle sign-in requests
@csrf_exempt  # Only use @csrf_exempt if absolutely necessary (e.g., in development)
def login_user(request):
    # Ensure request method is POST
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            # Validate that username and password are provided
            if not username or not password:
                logger.warning("Login attempt failed: missing credentials.")
                return JsonResponse({"error": "Username and password are required."}, status=400)

            # Try to authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # If user is valid, log them in
                login(request, user)
                logger.info(f"User {username} logged in successfully.")
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                # If authentication fails, log the attempt and return an error
                logger.warning(f"Login attempt failed for username: {username}")
                return JsonResponse({"error": "Invalid username or password."}, status=401)

        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from request body.")
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    else:
        # Return a method not allowed error if the request is not POST
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)


# Create a `logout_request` view to handle sign-out requests
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        logger.info("User logged out successfully.")
        return JsonResponse({"status": "Logged out"})
    else:
        # Return a method not allowed error if the request is not POST
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)


# Placeholder for `registration` view (uncomment and define the registration logic)
# @csrf_exempt
# def registration(request):
#     # Registration logic here
#     pass
@csrf_exempt
def registration(request):
    context = {}

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

# Placeholder for `get_dealerships` view (uncomment and define the view logic)
# def get_dealerships(request):
#     # Logic to get and display a list of dealerships
#     pass

# Placeholder for `get_dealer_reviews` view (uncomment and define the view logic)
# def get_dealer_reviews(request, dealer_id):
#     # Logic to get and display reviews of a dealer
#     pass

# Placeholder for `get_dealer_details` view (uncomment and define the view logic)
# def get_dealer_details(request, dealer_id):
#     # Logic to display details of a dealer
#     pass

# Placeholder for `add_review` view (uncomment and define the view logic)
# def add_review(request):
#     # Logic to submit a review
#     pass
