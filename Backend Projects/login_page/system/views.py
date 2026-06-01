from django.shortcuts import render, redirect
from .models import CustomUser

# 1. THE LOGIN GATE (Main Entrance - Handles GET view and POST authentication)
def login_view(request):
    error_message = None
    
    if request.method == "POST":
        # Extract plain strings from the HTML input 'name' keys
        login_user = request.POST.get('html_username')
        login_pass = request.POST.get('html_password')
        
        # Database Cross-Reference Check: Look for a row matching username AND password
        matched_user = CustomUser.objects.filter(username=login_user, password=login_pass).first()
        
        if matched_user:
            # Match found! Redirect straight to the showcase dashboard area
            return redirect('/dashboard/')
        else:
            # No row found. Deny access and refresh the page with an error string
            error_message = "❌ Invalid username or password. User record not found."
            
    return render(request, 'login.html', {'error': error_message})


# 2. THE REGISTRATION PORTAL (Account Creation Suite)
def registration_view(request):
    error_message = None
    
    if request.method == "POST":
        reg_user = request.POST.get('html_username')
        reg_pass = request.POST.get('html_password')
        
        # Query the database table to check if this username string is already taken
        username_exists = CustomUser.objects.filter(username=reg_user).exists()
        
        if username_exists:
            error_message = "❌ That username is already registered! Choose another."
        else:
            # Username is unique! Insert a fresh row record into the database table
            CustomUser.objects.create(
                username=reg_user,
                password=reg_pass
            )
            # Row committed. Redirect them immediately to the empty login page
            return redirect('/')
            
    return render(request, 'registration.html', {'error': error_message})


# 3. THE RANDOM SHOWCASE DASHBOARD (The Successful Reward Screen)
def dashboard_view(request):
    return render(request, 'dashboard.html')


# 4. THE EXIT DOOR (Wipes the State)
def logout_view(request):
    return redirect('/')