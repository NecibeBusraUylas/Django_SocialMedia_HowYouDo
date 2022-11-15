from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render
from .models import Profile, Post, LikePost, FollowersCount


# Create your views here.
@login_required(login_url='signin')
def index(request):
    # to get and show the profile image of the user
    user_object= User.objects.get(username=request.user.username) # get the object of currently log in user 
    user_profile = Profile.objects.get(user=user_object) # use object of the user to get profile information
    
    # to get and show the feed of the user
    feed_posts_lists = Post.objects.all()
    
    return render(request, 'index.html', {'user_profile': user_profile, 'feed_posts_lists': feed_posts_lists})

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

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username # to get username of currently log in user
    post_id = request.GET.get('post_id') # get the unique id of the post

    post = Post.objects.get(id=post_id) # get the informations of post using post's unique id

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first() # get if there is any data in db that matches the username and post

    if like_filter == None: # if user didn't like the post before user will like the post
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.number_of_likes = post.number_of_likes + 1
        post.save()
        return redirect('/')
    else:  # if user did like the post before user will dislike the post
        like_filter.delete()
        post.number_of_likes = post.number_of_likes - 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def profile(request, pk): # pk is the username of currently log in user
    # current user's informations
    current_user = User.objects.get(username=request.user.username)
    current_user_profile = Profile.objects.get(user=current_user)
    
    # to show the profile of user get all of the details of user 
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_number = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'current_user': current_user,
        'current_user_profile': current_user_profile,
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_number': user_post_number,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        # if there is any data in db that matches the follower and user then follower stop follow the user 
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:  # if none of the data in db matches with the follower and user then follower will follow the user
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
