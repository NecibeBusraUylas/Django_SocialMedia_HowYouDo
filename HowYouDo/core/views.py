from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2: # checks the password and confirm passwords are the same
            if User.objects.filter(email = email).exists(): # checks there is an email like we enter in db 
                messages.info(request, 'E-mail has already been used!')
                return redirect('signup')
            elif User.objects.filter(username = username).exists(): # checks there is an username like we enter in db
                messages.info(request, 'Username has already been used!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # log user in and redirect to setting page
                # create a profile object for the new user
                
                # for sending user the profile model
                user = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user,id_user=user.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password not matching!!!')
            return redirect('/signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is None:  # checks is there exist a user with entered information
            messages.info(request, 'Incorrect username or password!!!')
            return redirect('signin')
        else:
            auth.login(request, user)
            return redirect('/')
    else:
        return render(request, 'signin.html')
    
def logout(request):
    auth.logout(request)
    return redirect('signin')