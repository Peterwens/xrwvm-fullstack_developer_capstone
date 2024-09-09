from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging
import json
from datetime import datetime
from .models import CarMake, CarModel
from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)

#get car
def get_cars(request):
    try:
        count = CarMake.objects.count()
        logger.info(f"CarMake count: {count}")
        
        if count == 0:
            initiate()  # Populate the database if CarMake is empty

        car_models = CarModel.objects.select_related('car_make')
        cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
        
        return JsonResponse({"CarModels": cars})

    except Exception as e:
        logger.error(f"Error fetching car models: {e}")
        return JsonResponse({"error": "Something went wrong while fetching car data."}, status=500)


# Create a `login_request` view to handle sign-in requests
@csrf_exempt  # Only use @csrf_exempt if absolutely necessary (e.g., in development)
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            if not username or not password:
                logger.warning("Login attempt failed: missing credentials.")
                return JsonResponse({"error": "Username and password are required."}, status=400)

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"User {username} logged in successfully.")
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                logger.warning(f"Login attempt failed for username: {username}")
                return JsonResponse({"error": "Invalid username or password."}, status=401)

        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from request body.")
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

# Create a `logout_request` view to handle sign-out requests
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        logger.info("User logged out successfully.")
        return JsonResponse({"status": "Logged out"})
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

# Create a `registration` view to handle sign-up requests
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            if not username or not password or not email:
                return JsonResponse({"error": "All fields are required."}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Already Registered"}, status=400)

            # Create new user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )
            user.save()

            # Auto-login the user after registration
            login(request, user)
            logger.info(f"New user registered and logged in: {username}")
            return JsonResponse({"userName": username, "status": "Authenticated"}, status=200)

        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from request body.")
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

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
