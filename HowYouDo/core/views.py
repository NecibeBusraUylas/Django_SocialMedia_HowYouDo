from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render

from .models import Profile


# Create your views here.
@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2: # checks the password and confirm passwords are the same
            if User.objects.filter(email = email).exists(): # checks there is an email like we enter in db 
                messages.error(request, 'E-mail has already been used!')
                return redirect('signup')
            elif User.objects.filter(username = username).exists(): # checks there is an username like we enter in db
                messages.error(request, 'Username has already been used!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                # log user in and redirect to setting page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create a profile object for the new user
                user = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user,id_user=user.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.error(request, 'Password not matching!!!')
            return redirect('/signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is None:  # checks is there exist a user with entered information
            messages.error(request, 'Incorrect username or password!!!')
            return redirect('signin')
        else:
            auth.login(request, user)
            return redirect('/')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user) # getting the profile object in which the user the currently logged in user
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileImage # if user didn't summit image it's just getting the default image 
            about = request.POST['about']
            location = request.POST['location']
           
            user_profile.profileImage = image
            user_profile.about= about
            user_profile.location = location
            user_profile.save()
            
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')  # if user summit image it's getting the image
            about = request.POST['about']
            location = request.POST['location']
            
            user_profile.profileImage = image
            user_profile.about = about
            user_profile.location = location
            user_profile.save()
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile}) # pass the profile object to settings page