from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from people.models import People

def register_people(request):
    """Handle the registration of a new People user."""
    if request.method == 'POST':
        # Get form data
        lastname = request.POST.get('lastname')
        firstname = request.POST.get('firstname')
        birthday = request.POST.get('birthday')  # You may want to handle this field
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')

        # Validate passwords
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('register_people')

        # Create user
        user = User.objects.create_user(
            username=f"{firstname}_{lastname}",  # Create a unique username
            email=email,
            password=password1
        )

        # Create People instance
        People.objects.create(
            user=user,
            birthdayPeople=birthday,
            addressPeople='',  # You may want to add an address field in your form
            numberPeople=phone,
            indicatorPeople='+225'  # Default indicator
        )

        messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
        return redirect('home')  # Redirect to home or login page

    return render(request, 'html/authentication/signup.html')  # Update with your actual template path

def login_view(request):
    """Handle user login using email."""
    if request.method == 'POST':
        email_or_phone = request.POST.get('email')  # Get email input
        password = request.POST.get('password')

        # Attempt to find the user by email
        try:
            user = User.objects.get(email=email_or_phone)
            # Authenticate the user using the username and password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect('home')  # Redirect to home or dashboard after login
            else:
                messages.error(request, "Identifiants invalides. Veuillez réessayer.")
        except User.DoesNotExist:
            messages.error(request, "Identifiants invalides. Veuillez réessayer.")

    return render(request, 'html/authentication/signin.html')  # Update with your actual template path

def logout_view(request):
    """Handle user logout."""
    logout(request)  # Log the user out
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')  # Redirect to the home page or login page
